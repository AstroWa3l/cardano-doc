import streamlit as st
import pandas as pd
import numpy as np
import json
import pandas as pd
import numpy as np
import koios_python
import socket
import sys

kp = koios_python.URLs()

st.title('Cardano Stake Pool Doctor')
 
col1, col2 = st.columns(2)


with col1:
        if 'pool_id' not in st.session_state:
                st.session_state.pool_id = ''
        text_input = st.text_input(
	        "Enter Your Bech32 poolID Here 👇",
        )
        if text_input:
                st.session_state.pool_id = text_input
                st.write("Your poolID is: ", text_input)

        
def check_relays(pool_id_bech32):
        # get pool info from koios
        pool_info_df = pd.DataFrame(kp.get_pool_info(pool_id_bech32))
        
        #number of relays
        n = 0
        for relay in pool_info_df['relays'][0]:
                for key, value in relay.items():
                        pool_info_df[f'relay_{n}_{key}'] = [value]
                n += 1

        # loop through columns containing relay data
        for relay in pool_info_df['relays'][0]:
                soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                port = relay['port']
                if relay['ipv4'] != None:
                        hostname = relay['ipv4']
                if relay['ipv6'] != None:
                        hostname = relay['ipv6']
                if relay['dns'] != None:
                        hostname = relay['dns']
                if relay['srv'] != None:
                        hostname = relay['srv']
    
                print (f"checking {hostname} on port {port}")
        
                try:
                        # connecting to the host
                        soc.connect((hostname, port))
                        st.success("Success", icon="✅")
                        st.write (f"the socket has successfully connected to {hostname} on port {port}")
                        
                except socket.error:
                        st.write(f"the socket is not connected to {hostname} on port {port}")
                        # sys.exit()
                        
def check_pledge(pool_id_bech32):
        
        pool_info_df = pd.DataFrame(kp.get_pool_info(pool_id_bech32))
        owners = pool_info_df['owners'][0]
        owners_balances = [kp.get_account_info(owner)[0]['total_balance'] for owner in owners ]
        owners_balances = [int(balance) for balance in owners_balances]
        
        if sum(owners_balances) >= int(pool_info_df.pledge[0]):
                st.success("Pledge is met", icon='✅')
        else:
                st.error("Pledge is not met", icon='❌')
                
                        
with st.container():
	if text_input:
		check_relays(text_input)
		check_pledge(text_input)
        
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 