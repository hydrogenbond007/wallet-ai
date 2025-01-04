import os
from virtuals_sdk import game

# Initialize the WalletAI agent
agent = game.Agent(
    api_key=os.environ.get("VIRTUALS_API_KEY"),
    goal="Analyze crypto wallets and provide detailed portfolio insights with actionable recommendations",
    description="WalletAI: An expert crypto portfolio analyzer that provides detailed insights, charts, and actionable recommendations based on on-chain data",
    world_info="""
    You are WalletAI, an expert crypto wallet analyzer operating in the Web3 ecosystem.
    When users tag you with a wallet address, you analyze their portfolio and provide insights.
    
    Response Format:
    1. Performance chart comparing wallet vs ETH/BTC baseline
    2. 7-day performance highlights (biggest gainers/losers)
    3. Notable trading activity analysis
    4. Current portfolio allocation
    5. Actionable recommendations
    
    Context:
    - Author: {{author}}
    - Author Bio: {{bio}} 
    - Tweet Content: {{tweetContent}}
    - Conversation History: {{conversationHistory}}
    
    Task: {{task}}
    Reasoning: {{taskReasoning}}
    
    Guidelines:
    - Always be professional and data-driven
    - Provide clear, actionable insights
    - Use charts and metrics to support recommendations
    - Consider user's trading history and portfolio composition
    - Format responses for readability with bullet points and sections
    """
)

# Enable Twitter reply function
agent.use_default_twitter_functions(["reply_tweet"])

# Add wallet analysis function
wallet_analysis_fn = game.Function(
    fn_name="analyze_wallet",
    fn_description="Analyze wallet address for transaction history and performance metrics",
    args=[
        game.FunctionArgument(
            name="wallet_address",
            type="string",
            description="The wallet address to analyze"
        ),
        game.FunctionArgument(
            name="chain",
            type="string",
            description="The blockchain to analyze (e.g., base, ethereum)"
        )
    ],
    config=game.FunctionConfig(
        method="get",
        url="https://api.example.com/wallet-analysis",
        platform="twitter",
        headers={
            "Authorization": f"Bearer {os.environ.get('API_KEY')}",
            "Content-Type": "application/json"
        },
        success_feedback="Successfully analyzed wallet portfolio",
        error_feedback="Failed to analyze wallet: Please check the address and try again"
    )
)

# Add price fetching function
price_fetch_fn = game.Function(
    fn_name="fetch_prices",
    fn_description="Fetch current and historical prices for tokens",
    args=[
        game.FunctionArgument(
            name="token_addresses",
            type="array",
            description="List of token addresses to fetch prices for"
        )
    ],
    config=game.FunctionConfig(
        method="get",
        url="https://api.example.com/prices",
        platform="twitter",
        headers={
            "Authorization": f"Bearer {os.environ.get('API_KEY')}",
            "Content-Type": "application/json"
        },
        success_feedback="Successfully fetched token prices",
        error_feedback="Failed to fetch price data"
    )
)

# Add chart generation function
chart_fn = game.Function(
    fn_name="generate_chart",
    fn_description="Generate portfolio performance chart with ETH/BTC comparison",
    args=[
        game.FunctionArgument(
            name="wallet_data",
            type="string",
            description="Wallet performance data for visualization"
        )
    ],
    config=game.FunctionConfig(
        method="post",
        url="https://api.example.com/generate-chart",
        platform="twitter",
        headers={
            "Authorization": f"Bearer {os.environ.get('API_KEY')}",
            "Content-Type": "application/json"
        },
        success_feedback="Successfully generated performance chart",
        error_feedback="Failed to generate chart visualization"
    )
)

# Add recommendation function
recommend_fn = game.Function(
    fn_name="generate_recommendations",
    fn_description="Generate portfolio recommendations based on analysis",
    args=[
        game.FunctionArgument(
            name="analysis_data",
            type="string",
            description="Analyzed wallet data for generating recommendations"
        )
    ],
    config=game.FunctionConfig(
        method="post",
        url="https://api.example.com/recommendations",
        platform="twitter",
        headers={
            "Authorization": f"Bearer {os.environ.get('API_KEY')}",
            "Content-Type": "application/json"
        },
        success_feedback="Successfully generated recommendations",
        error_feedback="Failed to generate recommendations"
    )
)

# Add functions to agent
agent.add_custom_function(wallet_analysis_fn)
agent.add_custom_function(price_fetch_fn)
agent.add_custom_function(chart_fn)
agent.add_custom_function(recommend_fn)

# Handle mentions/reactions
def handle_mention(tweet_id):
    response = agent.react(
        session_id=tweet_id,
        platform="twitter",
        tweet_id=tweet_id,
        task="""
        1. Extract wallet address from tweet
        2. Analyze wallet performance and holdings
        3. Generate performance visualization
        4. Provide detailed analysis including:
           - 7-day performance metrics
           - Notable trades
           - Current allocation
           - Actionable recommendations
        5. Format response for Twitter with clear sections
        """
    )
    return response

# Simulation for testing
def run_simulation():
    return agent.simulate_twitter(session_id="test-session")

# Deploy agent
def deploy():
    return agent.deploy_twitter()

if __name__ == "__main__":
    # For testing
    simulation_response = run_simulation()
    print("Simulation response:", simulation_response)
    
    # For production deployment
    # deploy()
