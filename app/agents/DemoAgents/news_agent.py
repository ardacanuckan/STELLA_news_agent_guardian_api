import requests
from app.models.agent import Agent
from app.models.chat import Chat
from app.openai_client import OpenAIClient
from app.utils.request_builder import RequestBuilder

class NewsAgent(Agent):
    """
    A news agent that uses the Guardian API to get news information.
    """

    def __init__(self):
        super().__init__(
            agent_id='news_agent',
            name='NEWS',
            short_description='Fetch news data',
            long_description='Fetch latest news articles from the Guardian API',
            display_name='NEWS',
            connections_available={}
        )

    def respond(self, openai_client: OpenAIClient, request_builder: RequestBuilder, chat: Chat = None, memories=None):
        user_input = chat.latest_message if chat else ""
        if not user_input:
            return "Please provide a topic for the news."

        news_data = self.get_news(user_input)
        return news_data if news_data else "Sorry, I couldn't fetch the news at this moment."

    def get_news(self, topic):
        api_key = 'your_guardian_api_key'  # Replace with your Guardian API key
        url = f"https://content.guardianapis.com/search?q={topic}&api-key={api_key}"
        
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get('response', {}).get('results', [])
            if not articles:
                return "No articles found for this topic."
            
            news_str = ""
            for article in articles:
                news_str += f"Title: {article.get('webTitle')}\nURL: {article.get('webUrl')}\n\n"
            return news_str.strip()
        else:
            return "Error fetching news from the Guardian API."
