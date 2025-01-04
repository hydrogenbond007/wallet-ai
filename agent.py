import os
from virtuals_sdk import game, Agent

# Initialize the agent
agent = Agent(
    api_key=os.environ.get("VIRTUALS_API_KEY"),
    goal="Analyze crypto wallets and provide detailed portfolio analysis and recommendations",
    description="WalletAI: An expert crypto portfolio analyzer that provides detailed insights, charts, and actionable recommendations",
    world_info="Crypto trading environment with access to on-chain data, price feeds, and historical performance metrics"
)

agent.use_default_twitter_functions(["reply_tweet"])
# uses the basic twitter functions

#we need a lot better wallet analysing logic here, this is super barebones
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
        url="",
        platform="twitter",
        success_feedback="Wallet analysis completed successfully",
        error_feedback="Failed to analyze wallet"
    )
)

# Function to generate performance charts
generate_chart_fn = Agent.Function(
    fn_name="generate_chart",
    fn_description="Generate portfolio performance chart with ETH/BTC comparison",
    args=[
        game.FunctionArgument(
            name="wallet_data",
            type="string",
            description="Wallet performance data"
        )
    ],
    config=game.FunctionConfig(
        method="post",
        url="https://your-chart-api.com/generate",
        platform="twitter",
        success_feedback="Chart generated successfully",
        error_feedback="Failed to generate chart"
    )
)

# Function to generate portfolio recommendations
generate_recommendations_fn = game.Function(
    fn_name="generate_recommendations",
    fn_description="Generate portfolio recommendations based on analysis",
    args=[
        game.FunctionArgument(
            name="analysis_data",
            type="string",
            description="Analyzed wallet data"
        )
    ],
    config=game.FunctionConfig(
        method="post",
        url="api ",
        platform="twitter",
        success_feedback="Recommendations generated successfully",
        error_feedback="Failed to generate recommendations"
    )
)

def handle_mention(tweet_id):
    response = agent.react(
        session_id=tweet_id,  # Use tweet ID as session ID
        platform="twitter",
        tweet_id=tweet_id,
        task="""
        1. Extract wallet address and chain from the tweet
        2. Analyze the wallet's performance and holdings
        3. Generate performance chart
        4. Provide detailed analysis including:
           - 7-day performance highlights
           - Notable trades
           - Portfolio allocation
           - Actionable recommendations
        5. Reply with chart and analysis in a clear, formatted manner
        """
    )
    return response

# Example usage
tweet_id = "example_tweet_id"
handle_mention(tweet_id)

# Add custom functions to agent
agent.add_custom_function(wallet_analysis_fn)
agent.add_custom_function(generate_chart_fn)
agent.add_custom_function(generate_recommendations_fn)
