import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re

# Set page configuration
st.set_page_config(
    page_title="AI Coaching Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SIMULATED AI ANALYSIS FUNCTION (No OpenAI package needed!)
def simulate_ai_analysis(transcript, interaction_type, agent_name):
    """
    This function simulates AI analysis without needing the OpenAI package
    """
    # Simulate different analysis based on content
    transcript_lower = transcript.lower()
    
    if any(word in transcript_lower for word in ['frustrat', 'angry', 'upset', 'disappoint', 'unfair', 'complaint']):
        sentiment = "Negative"
        issues = ["Customer frustration not adequately addressed", "Empathy statements missing", "Opportunity to de-escalate was missed"]
        strengths = ["Professional tone maintained", "Accurate information provided", "Good product knowledge"]
        coaching_focus = "Practice empathy statements and de-escalation techniques"
        example_phrase = "\"I understand why that would be frustrating. Let me see what I can do to help resolve this for you.\""
        
    elif any(word in transcript_lower for word in ['thank', 'appreciate', 'helpful', 'great', 'perfect', 'awesome']):
        sentiment = "Positive"
        issues = ["Opportunity to upsell missed", "Could have asked for feedback or review"]
        strengths = ["Excellent customer service", "Strong problem resolution", "Positive customer feedback received"]
        coaching_focus = "Upselling techniques and feedback collection"
        example_phrase = "\"I'm so glad I could help! Would you be interested in our premium plan that prevents this issue in the future?\""
        
    else:
        sentiment = "Neutral"
        issues = ["Conversation could have been more engaging", "Missing opportunity to build rapport", "Proactive support could be improved"]
        strengths = ["Efficient handling of inquiry", "All procedures followed correctly", "Good documentation of the issue"]
        coaching_focus = "Building customer rapport and proactive engagement"
        example_phrase = "\"Is there anything else I can help you with today? I'm here to assist!\""

    # Generate realistic feedback
    feedback = f"""
**Agent:** {agent_name}
**Interaction Type:** {interaction_type}
**Overall Sentiment:** {sentiment}

## 🎯 Strengths:
{''.join([f'✅ {s}\\n' for s in strengths])}

## 📋 Areas for Improvement:
{''.join([f'⚠️ {i}\\n' for i in issues])}

## 🎓 Recommended Coaching Focus:
{coaching_focus}

## 💡 Example Phrasing:
{example_phrase}
"""
    
    return feedback, sentiment, strengths, issues

# Sample data for demonstration
@st.cache_data
def load_sample_data():
    agents = [
        {"id": 1, "name": "Sarah Johnson", "team": "Customer Support", "tenure": 18, "avg_rating": 4.2},
        {"id": 2, "name": "Michael Chen", "team": "Technical Support", "tenure": 6, "avg_rating": 3.8},
        {"id": 3, "name": "Jessica Williams", "team": "Sales", "tenure": 12, "avg_rating": 4.5},
        {"id": 4, "name": "David Smith", "team": "Customer Support", "tenure": 24, "avg_rating": 4.1},
        {"id": 5, "name": "Emily Rodriguez", "team": "Technical Support", "tenure": 3, "avg_rating": 3.5}
    ]
    
    interactions = []
    for i in range(50):
        agent = np.random.choice(agents)
        interaction_types = ["Call", "Chat", "Email"]
        sentiment = np.random.choice(["Positive", "Neutral", "Negative"], p=[0.6, 0.25, 0.15])
        
        interactions.append({
            "id": i + 1000,
            "agent_id": agent["id"],
            "agent_name": agent["name"],
            "type": np.random.choice(interaction_types),
            "date": datetime.now() - timedelta(days=np.random.randint(0, 30)),
            "duration": np.random.randint(60, 600) if np.random.random() > 0.3 else None,  # Some interactions might not have duration
            "customer_sentiment": sentiment,
            "resolution_status": np.random.choice(["Resolved", "Escalated", "Pending"], p=[0.7, 0.1, 0.2]),
            "topic": np.random.choice(["Billing", "Technical Issue", "Product Info", "Account Management", "Complaint"])
        })
    
    return pd.DataFrame(agents), pd.DataFrame(interactions)

# Main application
def main():
    st.title("🤖 AI-Enhanced Coaching & Feedback Tool")
    st.markdown("Leverage AI to analyze customer interactions and generate personalized coaching feedback for your team.")
    
    # Load sample data
    agents_df, interactions_df = load_sample_data()
    
    # Sidebar for navigation
    st.sidebar.header("Navigation")
    app_mode = st.sidebar.selectbox("Choose a view", 
                                   ["Dashboard", "Interaction Analysis", "Agent Performance", "Coaching Hub"])
    
    # Dashboard view
    if app_mode == "Dashboard":
        st.header("Team Performance Dashboard")
        
        # KPI metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Agents", len(agents_df))
        with col2:
            avg_rating = agents_df['avg_rating'].mean()
            st.metric("Average Rating", f"{avg_rating:.1f}/5.0")
        with col3:
            resolved = len(interactions_df[interactions_df['resolution_status'] == 'Resolved'])
            st.metric("Resolution Rate", f"{(resolved/len(interactions_df))*100:.1f}%")
        with col4:
            negative = len(interactions_df[interactions_df['customer_sentiment'] == 'Negative'])
            st.metric("Negative Sentiment", f"{(negative/len(interactions_df))*100:.1f}%")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Sentiment distribution
            sentiment_counts = interactions_df['customer_sentiment'].value_counts()
            fig = px.pie(values=sentiment_counts.values, 
                         names=sentiment_counts.index,
                         title="Customer Sentiment Distribution")
            st.plotly_chart(fig, use_container_width=True)
            
            # Interaction types
            type_counts = interactions_df['type'].value_counts()
            fig = px.bar(x=type_counts.index, y=type_counts.values,
                         title="Interactions by Type", labels={'x': 'Type', 'y': 'Count'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Performance by team
            team_stats = interactions_df.merge(agents_df, left_on='agent_id', right_on='id')
            team_sentiment = pd.crosstab(team_stats['team'], team_stats['customer_sentiment'])
            fig = px.bar(team_sentiment, title="Sentiment by Team", barmode='group')
            st.plotly_chart(fig, use_container_width=True)
            
            # Top agents by rating
            fig = px.bar(agents_df.sort_values('avg_rating', ascending=False).head(5),
                         x='name', y='avg_rating', title="Top Agents by Rating",
                         labels={'name': 'Agent', 'avg_rating': 'Average Rating'})
            st.plotly_chart(fig, use_container_width=True)
    
    # Interaction Analysis view
    elif app_mode == "Interaction Analysis":
        st.header("Interaction Analysis")
        
        # Sample interactions for demo
        sample_interactions = {
            "Call": "Customer: I'm calling about my bill, it seems higher than usual.\nAgent: I can help with that. Can you provide your account number?\nCustomer: It's 12345. I just don't understand why it's so high this month.\nAgent: I see your account. You have an additional data charge for exceeding your plan limit.\nCustomer: What? No one told me I was close to my limit! This is so frustrating.\nAgent: The system sends automated alerts. You should have received a text message.\nCustomer: I never got anything. This is unfair billing practice.\nAgent: I can see the alert was sent to 555-1234 on the 15th. Would you like to add a data pack to avoid future overages?",
            
            "Chat": "Customer: Hi, my internet has been dropping frequently for the past week\nAgent: Hello! I'm sorry to hear you're experiencing issues. Can you tell me more about what's happening?\nCustomer: It just randomly disconnects, especially during video calls. Very annoying.\nAgent: I understand how frustrating that must be. Let's run a quick diagnostic on your connection.\nCustomer: OK, what do I need to do?\nAgent: First, please restart your modem by unplugging it for 30 seconds and then plugging it back in.\nCustomer: I've done that already multiple times. It doesn't help.\nAgent: I see. Let me check for any known outages in your area...",
            
            "Email": "Subject: Refund Request\n\nDear Support Team,\n\nI recently canceled my subscription but continue to be charged. I've sent two previous emails about this issue but haven't received a resolution. This is completely unacceptable and if not resolved immediately, I will be filing a complaint with the Better Business Bureau.\n\nPlease process my refund immediately and confirm when it has been completed.\n\nSincerely,\nFrustrated Customer"
        }
        
        interaction_type = st.selectbox("Select Interaction Type", list(sample_interactions.keys()))
        
        # Display sample transcript
        st.subheader("Sample Interaction Transcript")
        transcript = st.text_area("Transcript", sample_interactions[interaction_type], height=200)
        
        # Select agent
        agent_name = st.selectbox("Select Agent", agents_df['name'].tolist())
        
        # Analyze button
        if st.button("Analyze Interaction", type="primary"):
            with st.spinner("Analyzing interaction with AI..."):
                feedback, sentiment, strengths, issues = simulate_ai_analysis(transcript, interaction_type, agent_name)
            
            st.success("Analysis complete!")
            
            # Display results in tabs
            tab1, tab2, tab3 = st.tabs(["Feedback Summary", "Strengths", "Areas for Improvement"])
            
            with tab1:
                st.subheader("AI-Generated Feedback")
                st.markdown(feedback)
                
                # Quick actions
                st.subheader("Next Steps")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("Save Feedback"):
                        st.success("Feedback saved to agent profile!")
                with col2:
                    if st.button("Schedule Coaching Session"):
                        st.success("Coaching session scheduled!")
                with col3:
                    if st.button("Create Action Plan"):
                        st.success("Action plan created!")
            
            with tab2:
                if strengths:
                    for strength in strengths:
                        st.success(f"✅ {strength}")
                else:
                    st.info("No specific strengths identified in this analysis.")
            
            with tab3:
                if issues:
                    for issue in issues:
                        st.error(f"⚠️ {issue}")
                else:
                    st.info("No critical issues identified in this analysis.")
    
    # Agent Performance view
    elif app_mode == "Agent Performance":
        st.header("Agent Performance")
        
        # Select agent
        selected_agent = st.selectbox("Select Agent", agents_df['name'].tolist())
        agent_data = agents_df[agents_df['name'] == selected_agent].iloc[0]
        agent_interactions = interactions_df[interactions_df['agent_name'] == selected_agent]
        
        # Display agent details
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Average Rating", agent_data['avg_rating'])
        with col2:
            st.metric("Tenure (months)", agent_data['tenure'])
        with col3:
            resolved = len(agent_interactions[agent_interactions['resolution_status'] == 'Resolved'])
            st.metric("Resolution Rate", f"{(resolved/len(agent_interactions))*100:.1f}%" if len(agent_interactions) > 0 else "N/A")
        with col4:
            negative = len(agent_interactions[agent_interactions['customer_sentiment'] == 'Negative'])
            st.metric("Negative Sentiment", f"{(negative/len(agent_interactions))*100:.1f}%" if len(agent_interactions) > 0 else "N/A")
        
        # Agent performance charts
        if len(agent_interactions) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                # Sentiment distribution for this agent
                sentiment_counts = agent_interactions['customer_sentiment'].value_counts()
                fig = px.pie(values=sentiment_counts.values, 
                             names=sentiment_counts.index,
                             title="Customer Sentiment Distribution")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Resolution status for this agent
                resolution_counts = agent_interactions['resolution_status'].value_counts()
                fig = px.bar(x=resolution_counts.index, y=resolution_counts.values,
                             title="Resolution Status", labels={'x': 'Status', 'y': 'Count'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Recent interactions table
            st.subheader("Recent Interactions")
            st.dataframe(agent_interactions.sort_values('date', ascending=False).head(10))
        else:
            st.info("No interactions found for this agent.")
    
    # Coaching Hub view
    elif app_mode == "Coaching Hub":
        st.header("Coaching Hub")
        
        # Identify coaching opportunities
        st.subheader("Coaching Opportunities")
        
        # Simple algorithm to identify agents who might need coaching
        coaching_candidates = []
        for _, agent in agents_df.iterrows():
            agent_ints = interactions_df[interactions_df['agent_name'] == agent['name']]
            if len(agent_ints) > 0:
                negative_pct = len(agent_ints[agent_ints['customer_sentiment'] == 'Negative']) / len(agent_ints)
                resolution_rate = len(agent_ints[agent_ints['resolution_status'] == 'Resolved']) / len(agent_ints)
                
                if negative_pct > 0.2 or resolution_rate < 0.6:
                    coaching_candidates.append({
                        'agent': agent['name'],
                        'negative_rate': f"{negative_pct*100:.1f}%",
                        'resolution_rate': f"{resolution_rate*100:.1f}%",
                        'priority': 'High' if negative_pct > 0.3 else 'Medium'
                    })
        
        if coaching_candidates:
            coaching_df = pd.DataFrame(coaching_candidates)
            st.dataframe(coaching_df.sort_values('priority'))
            
            # Select agent to create coaching plan
            selected_agent = st.selectbox("Select Agent to Coach", coaching_df['agent'].tolist())
            
            st.subheader(f"Coaching Plan for {selected_agent}")
            
            # AI-generated coaching plan
            if st.button("Generate Coaching Plan", type="primary"):
                with st.spinner("Creating personalized coaching plan..."):
                    # Simulated coaching plan
                    coaching_plan = f"""
                    # Coaching Plan for {selected_agent}
                    
                    ## Focus Areas
                    1. **Customer Empathy** - Practice acknowledging customer feelings before problem-solving
                    2. **First Contact Resolution** - Work on resolving issues during the first interaction
                    3. **Proactive Communication** - Improve keeping customers informed throughout the interaction
                    
                    ## Recommended Activities
                    - Role-playing exercises with difficult customer scenarios
                    - Review of 3 positive interaction examples from top performers
                    - Side-by-side coaching on next 3 customer interactions
                    - Training module on effective troubleshooting techniques
                    
                    ## Success Metrics
                    - Reduce negative sentiment by 25% within 30 days
                    - Improve resolution rate to 75% within 30 days
                    - Achieve customer satisfaction score of 4.0 or higher
                    
                    ## Next Steps
                    - Schedule weekly coaching sessions for the next month
                    - Review progress after 2 weeks
                    - Adjust plan based on results
                    """
                    
                    st.markdown(coaching_plan)
        else:
            st.success("No critical coaching opportunities identified. Team performance is within expected parameters.")

# Run the app
if __name__ == "__main__":
    main()