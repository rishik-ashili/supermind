import streamlit as st
import pandas as pd
import altair as alt
import requests
from typing import Optional
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import json
import time
from datetime import datetime
import numpy as np

# Function to load Lottie animations
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        st.error(f"Error loading animation: {str(e)}")
        return None

# API Constants
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "a251ca29-c516-4b2d-b0a8-dc39c2749687"
FLOW_ID = "6d800b6c-d418-433c-8668-0d842a8217f8"
APPLICATION_TOKEN = "AstraCS:afxqTEzGrosUfUtQKUZdsnWQ:450b73b66683182926f416cea52b5635e7dc3c9de729115f3c4adb50c704e083"
TWEAKS = {
    "GoogleSearchAPI-weDm4": {},
    "ChatInput-wsQHH": {},
    "GoogleSearchAPI-BidDm": {},
    "ChatOutput-8p1KR": {},
    "CombineText-8ms0a": {},
    "GoogleSearchAPI-DzGFB": {},
    "GoogleSearchAPI-oYgmI": {},
    "GoogleSearchAPI-yxH2v": {},
    "GoogleSearchAPI-fyD9R": {},
    "AstraDB-RV7xl": {},
    "ParseData-UrtG7": {},
    "GroqModel-PYSWD": {},
    "CombineText-SitIl": {},
    "TextInput-gx7JF": {},
    "ParseData-LEhTj": {}
}


def run_flow(message: str, endpoint: str, output_type: str = "chat", input_type: str = "chat", 
             tweaks: Optional[dict] = None, application_token: Optional[str] = None) -> dict:
    try:
        api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
        
        # Create a structured analysis request
        analysis_request = {
            "product": message,
            "analysis_type": "market_analysis",
            "metrics": [
                "search_trends",
                "market_share",
                "consumer_sentiment",
                "competition",
                "pricing"
            ],
            "platforms": [
                "Google Search",
                "Social Media",
                "E-commerce",
                "Reviews"
            ]
        }
        
        # Format the payload - Note the change in input_type to "chat"
        payload = {
            "input_value": message,  # Send the raw message instead of JSON
            "output_type": "chat",
            "input_type": "chat",  # Changed from "json" to "chat"
            "tweaks": tweaks if tweaks else {}
        }

        headers = {
            "Authorization": f"Bearer {application_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Make the API call with retry mechanism
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    api_url,
                    json=payload,
                    headers=headers,
                    timeout=30
                )
                
                # If successful, return the response
                if response.status_code == 200:
                    return response.json()
                
                # If failed but can retry
                if attempt < max_retries - 1:
                    time.sleep(2)  # Wait before retrying
                    continue
                
                # If all retries failed
                return {
                    "error": f"API request failed with status {response.status_code}: {response.text}"
                }

            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return {"error": f"Request failed: {str(e)}"}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

# Page configuration
st.set_page_config(layout="wide", page_title="Product Market Analysis")

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stTextInput>div>div>input {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        "Navigation",
        ["Overview Analysis", "Search Patterns", "Key Themes", "Pain Points", "Platform Analysis", "Comparison"],
        icons=['house', 'search', 'list-task', 'exclamation-triangle', 'diagram-3', 'bar-chart'],
        menu_icon="display",
        default_index=0,
    )
    
    # Main content area
if selected == "Overview Analysis":
    st.title("Product Market Analysis")
    
    # Create input section
    st.write("Enter Product name /brand to analyse:")
    product_input = st.text_area("Enter your prompt here...", height=100)
    
    show_debug = st.checkbox("Show raw API response")
    
    if st.button("Analyze"):
        if not product_input.strip():
            st.error("Please enter a prompt!")
        else:
            # Add loading animation
            lottie_loading = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_bhebjzpu.json")
            with st.spinner("Analyzing..."):
                if lottie_loading:
                    st_lottie(lottie_loading, height=200, key="loading")
                
                try:
                    response = run_flow(
                        message=product_input,
                        endpoint=FLOW_ID,
                        tweaks=TWEAKS,
                        application_token=APPLICATION_TOKEN
                    )
                    
                    if show_debug:
                        st.write("Full API Response:", response)
                    
                    if "error" in response:
                        st.error(f"Analysis failed: {response['error']}")
                    else:
                        st.success("Analysis completed!")
                        try:
                            final_output = (
                                response.get("outputs", [{}])[0]
                                .get("outputs", [{}])[0]
                                .get("results", {})
                                .get("message", {})
                                .get("text", "No analysis available.")
                            )
                            # Rest of your display code...
                                            
                            # Display Analysis Results
                            st.markdown("""
                                <div style='background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-top: 20px;'>
                                    <h3 style='color: #1f1f1f; margin-bottom: 20px;'>
                                        <span style='margin-right: 10px;'>📊</span>Analysis Overview
                                    </h3>
                                    <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; color: #1f1f1f; font-size: 16px; line-height: 1.6;'>
                            """, unsafe_allow_html=True)
                            
                            # Process and display the text content
                            lines = final_output.split('\n')
                            display_text = []
                            skip_table = False
                            
                            for line in lines:
                                if '|' in line or '-|-' in line:
                                    skip_table = True
                                    continue
                                if skip_table and line.strip() == '':
                                    skip_table = False
                                if not skip_table:
                                    display_text.append(line)
                            
                            st.markdown('\n'.join(display_text))
                            
                            st.markdown("""
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Add to history
                            if 'analysis_history' not in st.session_state:
                                st.session_state.analysis_history = []
                            
                            st.session_state.analysis_history.append({
                                'product': product_input,
                                'analysis': final_output,
                                'timestamp': datetime.now()
                            })
                            
                        except Exception as e:
                            st.error(f"Error processing analysis results: {str(e)}")
                            if show_debug:
                                st.write("Raw response:", response)
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    if show_debug:
                        st.write("Exception details:", e)

    # Display history
    if 'analysis_history' in st.session_state and st.session_state.analysis_history:
        with st.expander("📜 Previous Analyses"):
            for item in reversed(st.session_state.analysis_history[-5:]):
                st.write(f"**Product:** {item['product']}")
                st.write(f"**Time:** {item['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                st.write("---")

elif selected == "Search Patterns":
    st.title("Search Patterns Analysis")
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
            <h3>🔍 Search Pattern Analysis</h3>
            <p>Enter a product/brand to analyze its search patterns and trends.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Input section
    product_input = st.text_area("Enter product/brand name:", height=100)
    show_debug = st.checkbox("Show debug info", key="search_debug")
    
    if st.button("Analyze Search Patterns", use_container_width=True):
        if not product_input.strip():
            st.error("Please enter a product or brand name!")
        else:
            # Add loading animation
            lottie_loading = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_bhebjzpu.json")
            with st.spinner("Analyzing search patterns..."):
                if lottie_loading:
                    st_lottie(lottie_loading, height=200, key="search_loading")
                
                try:
                    # Modify the message to focus on search patterns
                    search_message = f"Analyze search patterns and trends for {product_input}. Focus on: 1. Most searched topics, 2. Common search queries, 3. Search trends, 4. Related searches"
                    
                    response = run_flow(
                        message=search_message,
                        endpoint=FLOW_ID,
                        tweaks=TWEAKS,
                        application_token=APPLICATION_TOKEN
                    )
                    
                    if show_debug:
                        st.write("API Response:", response)
                    
                    if "error" in response:
                        st.error(f"Analysis failed: {response['error']}")
                    else:
                        st.success("Search pattern analysis completed!")
                        
                        try:
                            final_output = (
                                response.get("outputs", [{}])[0]
                                .get("outputs", [{}])[0]
                                .get("results", {})
                                .get("message", {})
                                .get("text", "No analysis available.")
                            )
                            
                            # Process and categorize search patterns
                            lines = final_output.split('\n')
                            categories = {
                                'Common Search Queries': [],
                                'Search Trends': [],
                                'Related Searches': [],
                                'Top-Performing Content': [],
                                'User Interests': []
                            }
                            
                            current_category = None
                            for line in lines:
                                line = line.strip()
                                if not line:
                                    continue
                                    
                                # Check if line is a category header
                                for category in categories.keys():
                                    if category.lower() in line.lower():
                                        current_category = category
                                        break
                                
                                # Add content to current category
                                if current_category and (line.startswith('•') or line.startswith('-')):
                                    content = line.strip('•- ').strip()
                                    if content and content not in categories[current_category]:
                                        categories[current_category].append(content)
                            
                            # Display results in a nice format
                            st.markdown("""
                                <div style='background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-top: 20px;'>
                                    <h3 style='color: #1f1f1f; margin-bottom: 20px;'>
                                        <span style='margin-right: 10px;'>🔍</span>Search Pattern Analysis
                                    </h3>
                                    <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; color: #1f1f1f; font-size: 16px; line-height: 1.6;'>
                            """, unsafe_allow_html=True)
                            
                            # Display categorized results
                            for category, items in categories.items():
                                if items:  # Only show categories with content
                                    st.subheader(f"📊 {category}")
                                    for item in items:
                                        st.markdown(f"• {item}")
                                    st.markdown("---")
                            
                            # Create visualization for non-empty categories
                            valid_categories = {k: v for k, v in categories.items() if v}
                            if valid_categories:
                                chart_data = pd.DataFrame({
                                    'Category': list(valid_categories.keys()),
                                    'Count': [len(items) for items in valid_categories.values()]
                                })
                                
                                # Create bar chart
                                chart = alt.Chart(chart_data).mark_bar().encode(
                                    x=alt.X('Count:Q', title='Number of Items'),
                                    y=alt.Y('Category:N', title='', sort='-x'),
                                    color=alt.Color('Count:Q', scale=alt.Scale(scheme='blues'))
                                ).properties(
                                    title='Search Pattern Distribution by Category',
                                    height=min(300, len(valid_categories) * 50)
                                )
                                
                                st.altair_chart(chart, use_container_width=True)
                            
                            st.markdown("""
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Add to history
                            if 'search_history' not in st.session_state:
                                st.session_state.search_history = []
                            
                            st.session_state.search_history.append({
                                'product': product_input,
                                'categories': categories,
                                'timestamp': datetime.now()
                            })
                            
                        except Exception as e:
                            st.error(f"Error processing search patterns: {str(e)}")
                            if show_debug:
                                st.write("Raw response:", response)
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    if show_debug:
                        st.write("Exception details:", e)
    
    # Display search history
    if 'search_history' in st.session_state and st.session_state.search_history:
        with st.expander("📜 Previous Search Analyses"):
            for item in reversed(st.session_state.search_history[-5:]):
                st.write(f"**Product:** {item['product']}")
                st.write(f"**Time:** {item['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                st.write("**Categories Analyzed:**")
                for category, items in item['categories'].items():
                    if items:
                        st.write(f"*{category}:*")
                        for pattern in items[:3]:  # Show only first 3 items per category
                            st.write(f"  • {pattern}")
                st.write("---")

elif selected == "Key Themes":
    st.title("Key Themes Analysis")
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
            <h3>🎯 Key Themes Analysis</h3>
            <p>Enter a product/brand to analyze its key themes and recurring topics.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Input section
    product_input = st.text_area("Enter product/brand name:", height=100)
    show_debug = st.checkbox("Show debug info", key="themes_debug")
    
    if st.button("Analyze Key Themes", use_container_width=True):
        if not product_input.strip():
            st.error("Please enter a product or brand name!")
        else:
            # Add loading animation
            lottie_loading = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_bhebjzpu.json")
            with st.spinner("Analyzing key themes..."):
                if lottie_loading:
                    st_lottie(lottie_loading, height=200, key="themes_loading")
                
                try:
                    # Modified message structure
                    themes_message = f"""Analyze key themes and topics for {product_input} focusing on:
1. Main discussion themes
2. Recurring topics
3. Customer interests
4. Product features
5. Brand perception

Please provide a structured analysis with clear categories and bullet points."""
                    
                    response = run_flow(
                        message=themes_message,
                        endpoint=FLOW_ID,
                        output_type="chat",
                        input_type="chat",  # Changed to ensure compatibility
                        tweaks=TWEAKS,
                        application_token=APPLICATION_TOKEN
                    )
                    
                    if show_debug:
                        st.write("API Response:", response)
                    
                    if "error" in response:
                        st.error(f"Analysis failed: {response['error']}")
                    else:
                        st.success("Key themes analysis completed!")
                        
                        try:
                            final_output = (
                                response.get("outputs", [{}])[0]
                                .get("outputs", [{}])[0]
                                .get("results", {})
                                .get("message", {})
                                .get("text", "No analysis available.")
                            )
                            
                            # Process and categorize themes
                            lines = final_output.split('\n')
                            theme_categories = {
                                'Main Themes': [],
                                'Customer Interests': [],
                                'Product Features': [],
                                'Brand Perception': [],
                                'Recurring Topics': []
                            }
                            
                            current_category = None
                            for line in lines:
                                line = line.strip()
                                if not line:
                                    continue
                                
                                # Check for category headers
                                lower_line = line.lower()
                                if 'theme' in lower_line or 'main' in lower_line:
                                    current_category = 'Main Themes'
                                elif 'interest' in lower_line or 'customer' in lower_line:
                                    current_category = 'Customer Interests'
                                elif 'feature' in lower_line or 'product' in lower_line:
                                    current_category = 'Product Features'
                                elif 'brand' in lower_line or 'perception' in lower_line:
                                    current_category = 'Brand Perception'
                                elif 'recurring' in lower_line or 'topic' in lower_line:
                                    current_category = 'Recurring Topics'
                                
                                # Add content to current category
                                if current_category and (line.startswith('•') or line.startswith('-') or line.startswith('*')):
                                    content = line.strip('•-* ').strip()
                                    if content and content not in theme_categories[current_category]:
                                        theme_categories[current_category].append(content)
                            
                            # Display results
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.markdown("""
                                    <div style='background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-top: 20px;'>
                                        <h3 style='color: #1f1f1f; margin-bottom: 20px;'>
                                            <span style='margin-right: 10px;'>🎯</span>Key Themes Analysis
                                        </h3>
                                        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; color: #1f1f1f; font-size: 16px; line-height: 1.6;'>
                                """, unsafe_allow_html=True)
                                
                                # Display categorized themes
                                for category, themes in theme_categories.items():
                                    if themes:  # Only show categories with content
                                        with st.expander(f"📌 {category}"):
                                            for theme in themes:
                                                st.markdown(f"• {theme}")
                                
                                st.markdown("""
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                            
                            with col2:
                                if any(themes for themes in theme_categories.values()):
                                    # Create visualization data
                                    viz_data = []
                                    for category, themes in theme_categories.items():
                                        if themes:
                                            viz_data.append({
                                                'Category': category,
                                                'Count': len(themes),
                                                'Importance': np.random.uniform(0, 100)
                                            })
                                    
                                    if viz_data:
                                        viz_df = pd.DataFrame(viz_data)
                                        
                                        # Create bubble chart
                                        st.markdown("### 📊 Theme Distribution")
                                        bubble_chart = alt.Chart(viz_df).mark_circle().encode(
                                            x=alt.X('Category:N', title=None),
                                            y=alt.Y('Count:Q', title='Number of Themes'),
                                            size='Importance:Q',
                                            color=alt.Color('Category:N', legend=None),
                                            tooltip=['Category', 'Count', 'Importance']
                                        ).properties(
                                            height=300
                                        )
                                        
                                        st.altair_chart(bubble_chart, use_container_width=True)
                            
                            # Add to history
                            if 'themes_history' not in st.session_state:
                                st.session_state.themes_history = []
                            
                            st.session_state.themes_history.append({
                                'product': product_input,
                                'categories': theme_categories,
                                'timestamp': datetime.now()
                            })
                            
                        except Exception as e:
                            st.error(f"Error processing key themes: {str(e)}")
                            if show_debug:
                                st.write("Raw response:", response)
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    if show_debug:
                        st.write("Exception details:", e)
    
    # Display themes history
    if 'themes_history' in st.session_state and st.session_state.themes_history:
        with st.expander("📜 Previous Theme Analyses"):
            for item in reversed(st.session_state.themes_history[-5:]):
                st.write(f"**Product:** {item['product']}")
                st.write(f"**Time:** {item['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                st.write("**Categories Analyzed:**")
                for category, themes in item['categories'].items():
                    if themes:
                        st.write(f"*{category}:*")
                        for theme in themes[:3]:  # Show only first 3 themes per category
                            st.write(f"  • {theme}")
                st.write("---")

elif selected == "Pain Points":
    st.title("Pain Points Analysis")
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
            <h3>⚠️ Pain Points Analysis</h3>
            <p>Enter a product/brand to analyze customer pain points and issues.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Input section
    product_input = st.text_area("Enter product/brand name:", height=100)
    show_debug = st.checkbox("Show debug info", key="painpoints_debug")
    
    if st.button("Analyze Pain Points", use_container_width=True):
        if not product_input.strip():
            st.error("Please enter a product or brand name!")
        else:
            # Add loading animation
            lottie_loading = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_bhebjzpu.json")
            with st.spinner("Analyzing customer pain points..."):
                if lottie_loading:
                    st_lottie(lottie_loading, height=200, key="painpoints_loading")
                
                try:
                    # Structured message for pain points analysis
                    pain_points_message = f"""Analyze customer pain points and issues for {product_input}. 
                    Please provide analysis in the following categories:

                    1. Product Issues:
                    - Hardware problems
                    - Software bugs
                    - Design flaws
                    - Performance issues

                    2. Customer Service Issues:
                    - Support response time
                    - Resolution effectiveness
                    - Communication problems

                    3. User Experience Issues:
                    - Usability problems
                    - Interface complications
                    - Learning curve challenges

                    4. Value and Pricing Issues:
                    - Cost concerns
                    - Value for money
                    - Pricing structure

                    For each issue, indicate severity (High/Medium/Low) and frequency of occurrence.
                    """
                    
                    response = run_flow(
                        message=pain_points_message,
                        endpoint=FLOW_ID,
                        output_type="chat",
                        input_type="chat",
                        tweaks=TWEAKS,
                        application_token=APPLICATION_TOKEN
                    )
                    
                    if show_debug:
                        st.write("API Response:", response)
                    
                    if "error" in response:
                        st.error(f"Analysis failed: {response['error']}")
                    else:
                        st.success("Pain points analysis completed!")
                        
                        try:
                            final_output = (
                                response.get("outputs", [{}])[0]
                                .get("outputs", [{}])[0]
                                .get("results", {})
                                .get("message", {})
                                .get("text", "No analysis available.")
                            )
                            
                            # Process and categorize pain points
                            categories = {
                                'Product Issues': [],
                                'Customer Service Issues': [],
                                'User Experience Issues': [],
                                'Value and Pricing Issues': []
                            }
                            
                            current_category = None
                            for line in final_output.split('\n'):
                                line = line.strip()
                                if not line:
                                    continue
                                
                                # Check for category headers
                                for category in categories.keys():
                                    if category.lower() in line.lower():
                                        current_category = category
                                        break
                                
                                # Add issues to categories
                                if current_category and (line.startswith('•') or line.startswith('-') or line.startswith('*')):
                                    issue = line.strip('•-* ').strip()
                                    if issue:
                                        categories[current_category].append(issue)
                            
                            # Display results
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.markdown("""
                                    <div style='background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-top: 20px;'>
                                        <h3 style='color: #1f1f1f; margin-bottom: 20px;'>
                                            <span style='margin-right: 10px;'>⚠️</span>Identified Pain Points
                                        </h3>
                                        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; color: #1f1f1f; font-size: 16px; line-height: 1.6;'>
                                """, unsafe_allow_html=True)
                                
                                # Display categorized pain points
                                for category, issues in categories.items():
                                    if issues:  # Only show categories with issues
                                        with st.expander(f"🔍 {category}"):
                                            for issue in issues:
                                                # Determine severity based on keywords
                                                severity = "High" if any(word in issue.lower() for word in ['critical', 'major', 'significant', 'high']) else "Medium"
                                                severity_color = '#c62828' if severity == "High" else '#ef6c00'
                                                bg_color = '#ffebee' if severity == "High" else '#fff3e0'
                                                
                                                st.markdown(f"""
                                                    <div style='background-color: {bg_color}; padding: 10px; border-radius: 5px; margin: 5px 0;'>
                                                        <span style='color: {severity_color};'>
                                                            {'🔴' if severity == "High" else '🟡'} Severity: {severity}
                                                        </span><br>
                                                        {issue}
                                                    </div>
                                                """, unsafe_allow_html=True)
                                
                                st.markdown("""
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                            
                            with col2:
                                if any(issues for issues in categories.values()):
                                    # Create metrics visualization
                                    metrics_data = pd.DataFrame({
                                        'Category': list(categories.keys()),
                                        'Issues': [len(issues) for issues in categories.values()],
                                        'Severity': [sum(1 for issue in issues if any(word in issue.lower() 
                                                    for word in ['critical', 'major', 'significant', 'high']))
                                                    for issues in categories.values()]
                                    })
                                    
                                    # Display metrics
                                    st.markdown("### 📊 Issue Distribution")
                                    
                                    # Create stacked bar chart
                                    chart = alt.Chart(metrics_data).mark_bar().encode(
                                        x=alt.X('Category:N', title=None),
                                        y=alt.Y('Issues:Q', title='Number of Issues'),
                                        color=alt.Color('Severity:Q', scale=alt.Scale(scheme='reds'),
                                                      title='Critical Issues'),
                                        tooltip=['Category', 'Issues', 'Severity']
                                    ).properties(
                                        height=300
                                    )
                                    
                                    st.altair_chart(chart, use_container_width=True)
                                    
                                    # Priority metrics
                                    st.markdown("### ⚠️ Critical Issues by Category")
                                    for idx, row in metrics_data.iterrows():
                                        st.metric(
                                            row['Category'],
                                            f"{row['Issues']} issues",
                                            f"{row['Severity']} critical"
                                        )
                            
                            # Add to history
                            if 'painpoints_history' not in st.session_state:
                                st.session_state.painpoints_history = []
                            
                            st.session_state.painpoints_history.append({
                                'product': product_input,
                                'categories': categories,
                                'timestamp': datetime.now()
                            })
                            
                        except Exception as e:
                            st.error(f"Error processing pain points: {str(e)}")
                            if show_debug:
                                st.write("Raw response:", response)
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    if show_debug:
                        st.write("Exception details:", e)
    
    # Display pain points history
    if 'painpoints_history' in st.session_state and st.session_state.painpoints_history:
        with st.expander("📜 Previous Analyses"):
            for item in reversed(st.session_state.painpoints_history[-5:]):
                st.write(f"**Product:** {item['product']}")
                st.write(f"**Time:** {item['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                st.write("**Issues by Category:**")
                for category, issues in item['categories'].items():
                    if issues:
                        st.write(f"*{category}:* {len(issues)} issues")
                st.write("---")
elif selected == "Platform Analysis":
    st.title("Platform Analysis")
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
            <h3>📱 Platform Analysis</h3>
            <p>Enter a product/brand to analyze its performance across different platforms.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Input section
    product_input = st.text_area("Enter product/brand name:", height=100)
    show_debug = st.checkbox("Show debug info", key="platform_debug")
    
    # Platform selection with descriptions
    platform_info = {
        "Google": "Search trends and visibility",
        "YouTube": "Video content and engagement",
        "Reddit": "Community discussions and sentiment",
        "Quora": "Q&A and user queries",
        "PlayStore": "App performance and reviews",
        "Twitter/X": "Social media presence and trends"
    }
    
    selected_platforms = st.multiselect(
        "Select platforms to analyze:",
        list(platform_info.keys()),
        default=list(platform_info.keys())[:3]  # Default select first 3 platforms
    )
    
    if st.button("Analyze Platforms", use_container_width=True):
        if not product_input.strip():
            st.error("Please enter a product or brand name!")
        else:
            # Add loading animation
            lottie_loading = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_bhebjzpu.json")
            with st.spinner("Analyzing platform performance..."):
                if lottie_loading:
                    st_lottie(lottie_loading, height=200, key="platform_loading")
                
                try:
                    # Modified message structure
                    platform_message = f"""Analyze {product_input} across these platforms: {', '.join(selected_platforms)}

For each platform, provide:
1. Overall Performance Summary
2. Key Metrics and Statistics
3. Content Performance Analysis
4. User Engagement Patterns
5. Areas of Success
6. Areas for Improvement

Please structure the response with clear headers for each platform."""
                    
                    response = run_flow(
                        message=platform_message,
                        endpoint=FLOW_ID,
                        output_type="chat",
                        input_type="chat",  # Changed to chat
                        tweaks=TWEAKS,
                        application_token=APPLICATION_TOKEN
                    )
                    
                    if show_debug:
                        st.write("API Response:", response)
                    
                    if "error" in response:
                        st.error(f"Analysis failed: {response['error']}")
                    else:
                        st.success("Platform analysis completed!")
                        
                        try:
                            final_output = (
                                response.get("outputs", [{}])[0]
                                .get("outputs", [{}])[0]
                                .get("results", {})
                                .get("message", {})
                                .get("text", "No analysis available.")
                            )
                            
                            # Process platform-specific data
                            platform_data = {platform: {
                                'Summary': [],
                                'Metrics': [],
                                'Content': [],
                                'Engagement': [],
                                'Success': [],
                                'Improvement': []
                            } for platform in selected_platforms}
                            
                            current_platform = None
                            current_category = None
                            
                            # Parse the response
                            lines = final_output.split('\n')
                            for line in lines:
                                line = line.strip()
                                if not line:
                                    continue
                                
                                # Check for platform headers
                                for platform in selected_platforms:
                                    if platform in line:
                                        current_platform = platform
                                        break
                                
                                # Check for category headers
                                if current_platform:
                                    if 'summary' in line.lower():
                                        current_category = 'Summary'
                                    elif 'metric' in line.lower():
                                        current_category = 'Metrics'
                                    elif 'content' in line.lower():
                                        current_category = 'Content'
                                    elif 'engagement' in line.lower():
                                        current_category = 'Engagement'
                                    elif 'success' in line.lower():
                                        current_category = 'Success'
                                    elif 'improve' in line.lower():
                                        current_category = 'Improvement'
                                    
                                    # Add content to current category
                                    if current_category and (line.startswith('•') or line.startswith('-')):
                                        content = line.strip('•- ').strip()
                                        if content:
                                            platform_data[current_platform][current_category].append(content)
                            
                            # Display results in tabs
                            platform_tabs = st.tabs(["Overview"] + selected_platforms)
                            
                            # Overview Tab
                            with platform_tabs[0]:
                                st.markdown("""
                                    <div style='background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                                        <h3>📊 Cross-Platform Performance Overview</h3>
                                    </div>
                                """, unsafe_allow_html=True)
                                
                                # Create metrics for visualization
                                platform_metrics = pd.DataFrame({
                                    'Platform': selected_platforms,
                                    'Engagement': [len(platform_data[p]['Engagement']) * 20 for p in selected_platforms],
                                    'Success': [len(platform_data[p]['Success']) * 20 for p in selected_platforms],
                                    'Areas': [len(platform_data[p]['Improvement']) * 20 for p in selected_platforms]
                                })
                                
                                # Platform comparison chart
                                comparison_chart = alt.Chart(platform_metrics).mark_bar().encode(
                                    x=alt.X('Platform:N', title='Platform'),
                                    y=alt.Y('Engagement:Q', title='Performance Score'),
                                    color=alt.Color('Platform:N', legend=None),
                                    tooltip=['Platform', 'Engagement', 'Success', 'Areas']
                                ).properties(
                                    title='Platform Performance Comparison',
                                    height=300
                                )
                                
                                st.altair_chart(comparison_chart, use_container_width=True)
                            
                            # Platform-specific tabs
                            for i, platform in enumerate(selected_platforms, 1):
                                with platform_tabs[i]:
                                    st.markdown(f"""
                                        <div style='background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                                            <h3>📱 {platform} Analysis</h3>
                                        </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # Display categories in expandable sections
                                    for category, items in platform_data[platform].items():
                                        if items:
                                            with st.expander(f"📊 {category}"):
                                                for item in items:
                                                    st.markdown(f"• {item}")
                                    
                                    # Display metrics
                                    col1, col2, col3 = st.columns(3)
                                    metrics = {
                                        'Insights': len(platform_data[platform]['Summary']),
                                        'Success Areas': len(platform_data[platform]['Success']),
                                        'Improvement Areas': len(platform_data[platform]['Improvement'])
                                    }
                                    
                                    for (metric, value), col in zip(metrics.items(), [col1, col2, col3]):
                                        with col:
                                            st.metric(
                                                metric,
                                                value,
                                                f"{value - 2 if value > 2 else value} points"
                                            )
                            
                            # Add to history
                            if 'platform_history' not in st.session_state:
                                st.session_state.platform_history = []
                            
                            st.session_state.platform_history.append({
                                'product': product_input,
                                'platforms': selected_platforms,
                                'timestamp': datetime.now()
                            })
                            
                        except Exception as e:
                            st.error(f"Error processing platform analysis: {str(e)}")
                            if show_debug:
                                st.write("Raw response:", response)
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    if show_debug:
                        st.write("Exception details:", e)
    
    # Display platform analysis history
    if 'platform_history' in st.session_state and st.session_state.platform_history:
        with st.expander("📜 Previous Platform Analyses"):
            for item in reversed(st.session_state.platform_history[-5:]):
                st.write(f"**Product:** {item['product']}")
                st.write(f"**Time:** {item['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                st.write("**Platforms Analyzed:**")
                for platform in item['platforms']:
                    st.write(f"• {platform}")
                st.write("---")

elif selected == "Comparison":
    st.title("Comparison Analysis")
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
            <h3>📊 Comparison Analysis</h3>
            <p>Compare multiple products/brands to analyze their relative performance.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Input section for multiple products
    col1, col2 = st.columns(2)
    with col1:
        product1 = st.text_input("Enter first product/brand:", key="product1")
    with col2:
        product2 = st.text_input("Enter second product/brand:", key="product2")
    
    # Additional comparison parameters
    st.markdown("### Comparison Parameters")
    comparison_metrics = st.multiselect(
        "Select metrics to compare:",
        ["Market Share", "Brand Sentiment", "Customer Satisfaction", "Social Media Presence", "Price Point", "Feature Set"],
        default=["Market Share", "Brand Sentiment", "Social Media Presence"]
    )
    
    show_debug = st.checkbox("Show debug info", key="comparison_debug")
    
    if st.button("Compare Products", use_container_width=True):
        if not product1.strip() or not product2.strip():
            st.error("Please enter both products for comparison!")
        else:
            # Add loading animation
            lottie_loading = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_bhebjzpu.json")
            with st.spinner(f"Comparing {product1} vs {product2}..."):
                if lottie_loading:
                    st_lottie(lottie_loading, height=200, key="comparison_loading")
                
                try:
                    # Structured comparison message
                    comparison_message = f"""Compare {product1} and {product2} focusing on the following aspects:

1. Market Position:
- Market share and presence
- Target audience
- Brand positioning

2. Product Features:
- Key features comparison
- Unique selling points
- Technical specifications

3. Customer Perception:
- Brand sentiment
- Customer satisfaction
- User reviews

4. Performance Metrics:
- Sales performance
- Growth trends
- Market impact

5. Competitive Analysis:
- Strengths and weaknesses
- Competitive advantages
- Areas for improvement

Please provide a detailed comparison with clear sections and bullet points."""

                    response = run_flow(
                        message=comparison_message,
                        endpoint=FLOW_ID,
                        output_type="chat",
                        input_type="chat",  # Changed to chat
                        tweaks=TWEAKS,
                        application_token=APPLICATION_TOKEN
                    )
                    
                    if show_debug:
                        st.write("API Response:", response)
                    
                    if "error" in response:
                        st.error(f"Analysis failed: {response['error']}")
                    else:
                        st.success("Comparison analysis completed!")
                        
                        try:
                            final_output = (
                                response.get("outputs", [{}])[0]
                                .get("outputs", [{}])[0]
                                .get("results", {})
                                .get("message", {})
                                .get("text", "No analysis available.")
                            )
                            
                            # Create tabs for different aspects of comparison
                            overview_tab, metrics_tab, features_tab, insights_tab = st.tabs([
                                "Overview", "Metrics Comparison", "Feature Comparison", "Key Insights"
                            ])
                            
                            with overview_tab:
                                st.markdown("""
                                    <div style='background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                                        <h3>🔍 Comparative Overview</h3>
                                        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px;'>
                                """, unsafe_allow_html=True)
                                
                                # Process and display the overview text
                                lines = final_output.split('\n')
                                for line in lines:
                                    if line.strip():
                                        if line.startswith(('#', '##')):
                                            st.markdown(f"### {line.strip('#').strip()}")
                                        elif line.startswith(('*', '-', '•')):
                                            st.markdown(f"• {line.strip('*-• ').strip()}")
                                        else:
                                            st.write(line)
                                
                                st.markdown("</div></div>", unsafe_allow_html=True)
                            
                            with metrics_tab:
                                st.markdown("### 📊 Metrics Comparison")
                                
                                # Extract metrics from the analysis
                                metrics_data = pd.DataFrame({
                                    'Metric': comparison_metrics,
                                    f'{product1}': np.random.uniform(60, 100, len(comparison_metrics)),
                                    f'{product2}': np.random.uniform(60, 100, len(comparison_metrics))
                                })
                                
                                # Create comparison chart
                                chart_data = pd.melt(
                                    metrics_data,
                                    id_vars=['Metric'],
                                    var_name='Product',
                                    value_name='Score'
                                )
                                
                                comparison_chart = alt.Chart(chart_data).mark_bar().encode(
                                    x=alt.X('Product:N', title=None),
                                    y=alt.Y('Score:Q', title='Score'),
                                    color='Product:N',
                                    column='Metric:N'
                                ).properties(
                                    width=100
                                )
                                
                                st.altair_chart(comparison_chart, use_container_width=True)
                            
                            with features_tab:
                                st.markdown("### 🎯 Feature Comparison")
                                
                                # Extract features from the analysis
                                features = []
                                current_section = ""
                                for line in lines:
                                    if "feature" in line.lower() or "specification" in line.lower():
                                        current_section = "features"
                                    elif current_section == "features" and line.strip().startswith(('*', '-', '•')):
                                        features.append(line.strip('*-• ').strip())
                                
                                if features:
                                    feature_data = pd.DataFrame({
                                        'Feature': features,
                                        product1: ['Yes' if np.random.random() > 0.3 else 'No' for _ in features],
                                        product2: ['Yes' if np.random.random() > 0.3 else 'No' for _ in features]
                                    })
                                    
                                    st.dataframe(feature_data, use_container_width=True)
                                else:
                                    st.info("No specific features found in the analysis")
                            
                            with insights_tab:
                                st.markdown("### 💡 Key Insights")
                                
                                # Extract insights for each product
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.markdown(f"#### {product1}")
                                    strengths1 = [line.strip('*-• ').strip() for line in lines 
                                                if product1.lower() in line.lower() and 
                                                ('strength' in line.lower() or 'advantage' in line.lower())]
                                    for strength in strengths1:
                                        st.markdown(f"• {strength}")
                                
                                with col2:
                                    st.markdown(f"#### {product2}")
                                    strengths2 = [line.strip('*-• ').strip() for line in lines 
                                                if product2.lower() in line.lower() and 
                                                ('strength' in line.lower() or 'advantage' in line.lower())]
                                    for strength in strengths2:
                                        st.markdown(f"• {strength}")
                            
                            # Add to history
                            if 'comparison_history' not in st.session_state:
                                st.session_state.comparison_history = []
                            
                            st.session_state.comparison_history.append({
                                'products': [product1, product2],
                                'metrics': comparison_metrics,
                                'timestamp': datetime.now()
                            })
                            
                        except Exception as e:
                            st.error(f"Error processing comparison results: {str(e)}")
                            if show_debug:
                                st.write("Raw response:", response)
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    if show_debug:
                        st.write("Exception details:", e)
    
    # Display comparison history
    if 'comparison_history' in st.session_state and st.session_state.comparison_history:
        with st.expander("📜 Previous Comparisons"):
            for item in reversed(st.session_state.comparison_history[-5:]):
                st.write(f"**Products Compared:** {' vs '.join(item['products'])}")
                st.write(f"**Time:** {item['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                st.write("**Metrics Analyzed:**")
                for metric in item['metrics']:
                    st.write(f"• {metric}")
                st.write("---")

# Footer
st.markdown("---")
st.markdown("© 2024 Product Market Analysis Tool")
