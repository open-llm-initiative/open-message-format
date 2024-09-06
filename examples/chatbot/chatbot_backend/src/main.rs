use actix_web::{
    post,
    web::{self},
    App, HttpResponse, HttpServer, Responder,
};
use dotenv::dotenv;
use reqwest::{
    header::{HeaderMap, HeaderValue, CONTENT_TYPE},
    Client,
};
use serde::{Deserialize, Serialize};
use std::{
    env,
    io::{self, Write},
    sync::{Arc, RwLock},
    thread,
};

#[derive(Deserialize, Serialize, Debug)]
struct ImageSource {
    #[serde(rename = "type")]
    source_type: String, // e.g., "base64"
    media_type: String, // e.g., "image/jpeg"
    data: String,       // Base64-encoded image data
}

#[derive(Deserialize, Serialize, Debug)]
struct ImageUrl {
    url: String,
}

#[derive(Deserialize, Serialize, Debug)]
#[serde(tag = "type", rename_all = "snake_case")]
enum ContentItem {
    Text { text: String },
    Image { source: ImageSource },
    ImageUrl { image_url: ImageUrl },
}

#[derive(Deserialize, Serialize, Debug)]
#[serde(untagged)]
enum MessageContent {
    StringContent(String),
    ObjectContent(Vec<ContentItem>),
}

#[derive(Deserialize, Serialize, Debug)]
struct Message {
    role: String,
    content: MessageContent,
}
#[derive(Serialize, Deserialize)]
struct MessageResponse {
    content: String,
    refusal: Option<String>,
    role: String,
}

enum Provider {
    OpenAI,
    Anthropic,
    Mistral,
}

#[post("/message")]
async fn message_endpoint(
    state: web::Data<AppState>,
    item: web::Json<Vec<Message>>,
) -> impl Responder {
    let provider = state.provider.read().unwrap();

    let response = match *provider {
        Provider::OpenAI => prompt_openai(&item).await,
        Provider::Anthropic => prompt_anthropic(&item).await,
        Provider::Mistral => prompt_mistral(&item).await,
    };
    match response {
        Ok(content) => HttpResponse::Ok().json(content),
        Err(e) => HttpResponse::BadRequest().body(e.to_string()),
    }
}

struct AppState {
    provider: Arc<RwLock<Provider>>,
}

fn start_cli(provider: Arc<RwLock<Provider>>) {
    thread::spawn(move || loop {
        print!("Enter provider (openai/anthropic/mistral): ");
        io::stdout().flush().unwrap();

        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();

        let trimmed_input = input.trim();
        let mut provider_write = provider.write().unwrap();

        match trimmed_input {
            "openai" => {
                *provider_write = Provider::OpenAI;
                println!("Switched to OpenAI");
            }
            "anthropic" => {
                *provider_write = Provider::Anthropic;
                println!("Switched to Anthropic");
            }
            "mistral" => {
                *provider_write = Provider::Mistral;
                println!("Switched to Mistral");
            }
            _ => println!("Invalid provider. Please enter 'openai' or 'anthropic'."),
        }
    });
}

#[allow(dead_code)]
async fn prompt_openai(
    messages: &[Message],
) -> Result<MessageResponse, Box<dyn std::error::Error>> {
    // Load API key from environment
    let api_key = env::var("OPENAI_API_KEY")?;

    // Create an HTTP client
    let client = Client::new();

    // Define the request body for OpenAI
    let body = serde_json::json!({
        "model": "gpt-4o-mini",  // Replace with your desired model
        "messages": messages
    });

    // Send the request to OpenAI
    let response = client
        .post("https://api.openai.com/v1/chat/completions")
        .bearer_auth(api_key)
        .json(&body)
        .send()
        .await?;

    // Parse the response directly into MessageResponse
    let response_json: serde_json::Value = response.json().await?;
    let response_message: MessageResponse = serde_json::from_value(
        response_json
            .get("choices")
            .and_then(|choices| choices.get(0))
            .and_then(|choice| choice.get("message").cloned())
            .ok_or("Failed to parse OpenAI response")?,
    )?;

    Ok(response_message)
}

#[allow(dead_code)]
async fn prompt_anthropic(
    messages: &[Message],
) -> Result<MessageResponse, Box<dyn std::error::Error>> {
    // Load API key from environment
    let api_key = env::var("ANTHROPIC_API_KEY")?;

    // Set up the headers
    let mut headers = HeaderMap::new();
    headers.insert("x-api-key", HeaderValue::from_str(&api_key)?);
    headers.insert("anthropic-version", HeaderValue::from_static("2023-06-01"));
    headers.insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));

    // Create an HTTP client
    let client = Client::new();

    // Define the request body for Anthropic
    let body = serde_json::json!({
        "model": "claude-3-haiku-20240307",  // Replace with the appropriate model from Anthropic
        "messages": messages,  // Pass the messages directly
        "max_tokens": 1024
    });

    // Send the request to Anthropic
    let response = client
        .post("https://api.anthropic.com/v1/messages") // Correct endpoint for Anthropic API
        .headers(headers)
        .json(&body)
        .send()
        .await?;

    // Parse the response and extract the "content" field
    let response_json: serde_json::Value = response.json().await?;
    let response_text =
        response_json
            .get("content")
            .and_then(|content| content.get(0))
            .and_then(|texts| texts.get("text"))
            .and_then(|text| text.as_str())
            .ok_or("Failed to parse Anthropic response")?;

    // Construct the MessageResponse object
    let response_message = MessageResponse {
        content: response_text.to_string(),
        refusal: None,
        role: "assistant".to_string(),
    };

    Ok(response_message)
}

#[allow(dead_code)]
async fn prompt_mistral(
    messages: &[Message],
) -> Result<MessageResponse, Box<dyn std::error::Error>> {
    // Load API key from environment
    let api_key = env::var("MISTRAL_API_KEY")?;

    let mut headers = HeaderMap::new();
    headers.insert("Accept", HeaderValue::from_static("application/json"));
    headers.insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));

    // Create an HTTP client
    let client = Client::new();

    let body = serde_json::json!({
        "model": "open-mistral-nemo",  // Replace with your desired model
        "messages": messages
    });

    let response = client
        .post("https://api.mistral.ai/v1/chat/completions")
        .headers(headers)
        .bearer_auth(api_key)
        .json(&body)
        .send()
        .await?;

    let response_json: serde_json::Value = response.json().await?;

    let response_text = response_json
        .get("choices")
        .and_then(|choices| choices.get(0))
        .and_then(|choice| choice.get("message"))
        .and_then(|content| content.get("content"))
        .and_then(|text| text.as_str())
        .ok_or("Failed to parse Mistral response")?;

    let response_message = MessageResponse {
        content: response_text.to_string(),
        refusal: None,
        role: "assistant".to_string(),
    };

    Ok(response_message)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    dotenv().ok();

    let provider = Arc::new(RwLock::new(Provider::OpenAI));

    let state = web::Data::new(AppState {
        provider: provider.clone(),
    });

    // Start the CLI in a separate thread
    start_cli(provider);

    HttpServer::new(move || App::new().app_data(state.clone()).service(message_endpoint))
        .bind("127.0.0.1:8080")?
        .run()
        .await
}
