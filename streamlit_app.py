# Import necessary libraries
import streamlit as st
from agent_model import CustomModel
import pandas as pd
import numpy as np
import plotly.express as px
import time
import plotly.graph_objects as go

def get_user_preferences(num_agents):
    st.sidebar.subheader("Preferred Locations for Agents:")
    preferences = []
    for i in range(num_agents):
        x = st.sidebar.slider(f"x-coordinate for Agent {i + 1}:", min_value=1, max_value=10, value=5)
        y = st.sidebar.slider(f"y-coordinate for Agent {i + 1}:", min_value=1, max_value=10, value=5)
        preferences.append((x, y))
    return preferences

def plot_preferences(preferences, step):
    df = pd.DataFrame(preferences, columns=["X", "Y"])
    st.write(f"Agent Positions at Step {step}")
    st.dataframe(df)


def main():
    st.sidebar.title("Agent-Based Model Simulation")
    
    num_agents = st.sidebar.slider("Select the number of agents:", 1, 10, 5)
    grid_size = 10  # Assuming a 10x10 grid for simplicity
    user_preferences = get_user_preferences(num_agents)

    if st.sidebar.button("Start Simulation"):
        with st.empty():  # Use st.empty to update the plot in place
            model = CustomModel(grid_size, grid_size, num_agents, user_preferences)
            steps = 50  # Define the number of steps the simulation will run
            all_positions = []  # This will include agent ID now

            for step in range(steps):
                model.step()
                positions = model.all_positions[-1]
                # Include agent ID in the positions record
                for agent_id, pos in enumerate(positions, start=1):  # Start IDs at 1
                    all_positions.append((agent_id, pos[0], pos[1], step))
                
                df = pd.DataFrame(all_positions, columns=['agent_id', 'x', 'y', 'step'])
                # Using Plotly Express for dynamic coloring and Plotly Graph Objects for labels
                fig = go.Figure()
                for agent_id in df['agent_id'].unique():
                    agent_df = df[df['agent_id'] == agent_id]
                    fig.add_trace(go.Scatter(x=agent_df['x'], y=agent_df['y'], mode='lines+markers',
                                             marker=dict(size=12, opacity=0.25, color=px.colors.qualitative.Plotly[(agent_id - 1) % len(px.colors.qualitative.Plotly)], showscale=False),
                                             name=f'Agent {agent_id} Path'))
                    
                    starting_point = agent_df[agent_df['step'] == agent_df['step'].min()]
                    fig.add_trace(go.Scatter(x=starting_point['x'], y=starting_point['y'], mode='markers',
                                            marker=dict(size=14, symbol='diamond-cross-open', line=dict(width=2),color=px.colors.qualitative.Plotly[(agent_id - 1) % len(px.colors.qualitative.Plotly)]),
                                            name=f'Agent {agent_id} Start'))                
                
                fig.update_layout(title=f'Step {step + 1}', xaxis=dict(range=[0, grid_size]), yaxis=dict(range=[0, grid_size]),
                                  legend_title_text='Agent ID')
                st.plotly_chart(fig)
                
                time.sleep(0.5)  # Add a small delay to see the plot update

if __name__ == "__main__":
    main()
