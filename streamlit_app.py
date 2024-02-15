
import streamlit as st
from agent_model import CustomModel
import pandas as pd
import plotly.graph_objects as go
import time


st.set_page_config(page_title="Agent-Based Model Simulation", layout="centered")

def get_user_preferences(num_agents):
    st.subheader("Preferred Locations for Agents:")
    preferences = []
    for i in range(num_agents):
        x = st.slider(f"x-coordinate for Agent {i + 1}:", min_value=1, max_value=10, value=5, key=f"x{i}")
        y = st.slider(f"y-coordinate for Agent {i + 1}:", min_value=1, max_value=10, value=5, key=f"y{i}")
        preferences.append((x, y))
    return preferences

def main():
    st.title("Agent-Based Model Simulation")
    num_agents = st.slider("Select the number of agents:", 1, 10, 5)
    grid_size = 10  
    user_preferences = get_user_preferences(num_agents)

    if st.button("Start Simulation"):
        with st.empty():  
            model = CustomModel(grid_size, grid_size, num_agents, user_preferences)
            steps = 50  
            all_positions = [] 

            for step in range(steps):
                model.step()
                positions = model.all_positions[-1]
               
                for agent_id, pos in enumerate(positions, start=1): 
                    all_positions.append((agent_id, pos[0], pos[1], step))
                
                df = pd.DataFrame(all_positions, columns=['agent_id', 'x', 'y', 'step'])
                fig = go.Figure()
                for agent_id in df['agent_id'].unique():
                    agent_df = df[df['agent_id'] == agent_id]
                    fig.add_trace(go.Scatter(x=agent_df['x'], y=agent_df['y'], mode='lines+markers',
                                             marker=dict(size=12, opacity=0.5),
                                             name=f'Agent {agent_id} Path'))
                    starting_point = agent_df[agent_df['step'] == agent_df['step'].min()]
                    fig.add_trace(go.Scatter(x=starting_point['x'], y=starting_point['y'], mode='markers',
                                             marker=dict(size=14, symbol='diamond-tall', line=dict(width=2)),
                                             name=f'Agent {agent_id} Start'))
                
                st.plotly_chart(fig, use_container_width=True)  
                time.sleep(0.5)                    
                             
                fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), autosize=True,
                                  title=f'Step {step + 1}', xaxis=dict(range=[0, grid_size]), 
                                  legend=dict(
                                         font=dict(
                                     size=15,
                                        )),
                                  yaxis=dict(range=[0, grid_size]), legend_title_text='Agent ID')
            
if __name__ == "__main__":
    main()
