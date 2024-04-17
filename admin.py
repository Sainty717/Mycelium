import streamlit as st
import json
import os
import time

# Function to load JSON files
def load_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

# Function to save JSON files
def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Function to handle node removal
def remove_node(nodes_data, node_id):
    nodes_data = [node for node in nodes_data if node['id'] != node_id]
    return nodes_data

# Function to handle link removal
def remove_link(links_data, link_index):
    del links_data[link_index]
    return links_data

# Function to update PDF files
def update_pdf(nodes_data, node_id, new_pdf):
    pdf_dir = "pdfs"
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_file_path = f"{pdf_dir}/{node_id.replace(' ', '_')}.pdf"
    with open(pdf_file_path, 'wb') as f:
        f.write(new_pdf.getvalue())
    return pdf_file_path

# Function to update links with new node names
def update_links(links_data, old_node_name, new_node_name):
    updated_links_data = []
    for link in links_data:
        if link['source'] == old_node_name:
            link['source'] = new_node_name
        if link['target'] == old_node_name:
            link['target'] = new_node_name
        updated_links_data.append(link)
    return updated_links_data

# Streamlit app
def main():
    st.title('Mycelium')

    # Convert SVG to PNG
    png_path = "path1.png"

    # Load PNG image
    logo = open(png_path, "rb").read()

    # Display PNG image with adjusted width and alignment
    st.sidebar.image(logo, width=100)  # Adjust width and alignment as needed

    # Load data
    nodes_data = load_json('nodes.json')
    links_data = load_json('links.json')
    key_data = load_json('key.json')

    # Sidebar panel
    st.sidebar.header('Node Management')
    
    # Node Removal
    st.sidebar.subheader('Node Removal')
    node_to_remove = st.sidebar.selectbox('Select Node to Remove', [''] + [node['id'] for node in nodes_data])
    if st.sidebar.button('Remove Node'):
        if node_to_remove:
            nodes_data = remove_node(nodes_data, node_to_remove)
            links_data = [link for link in links_data if link['source'] != node_to_remove and link['target'] != node_to_remove]
            save_json(nodes_data, 'nodes.json')
            save_json(links_data, 'links.json')
            # Remove associated PDF file
            pdf_file_path = f"pdfs/{node_to_remove.replace(' ', '_')}.pdf"
            if os.path.exists(pdf_file_path):
                os.remove(pdf_file_path)
            st.sidebar.success('Node and associated links removed successfully!')
            time.sleep(1)
            st.experimental_rerun()
        else:
            st.sidebar.warning('Please select a node to remove.')

    # Change Node Name
    st.sidebar.subheader('Change Node Name')
    selected_node_for_name_change = st.sidebar.selectbox('Select Node', [''] + [node['id'] for node in nodes_data], key='select_node_name')
    if selected_node_for_name_change:
        new_node_name = st.sidebar.text_input('New Node Name', value=selected_node_for_name_change, key='new_node_name_input')
        if st.sidebar.button('Change Name', key='change_name_button'):
            if new_node_name:
                # Change node name
                node_index = next((index for index, node in enumerate(nodes_data) if node['id'] == selected_node_for_name_change), None)
                if node_index is not None:
                    old_node_name = nodes_data[node_index]['id']
                    nodes_data[node_index]['id'] = new_node_name
                    save_json(nodes_data, 'nodes.json')

                    # Rename associated PDF file
                    old_pdf_path = f"pdfs/{old_node_name.replace(' ', '_')}.pdf"
                    new_pdf_path = f"pdfs/{new_node_name.replace(' ', '_')}.pdf"
                    if os.path.exists(old_pdf_path):
                        os.rename(old_pdf_path, new_pdf_path)
                    
                    # Update links with new node name
                    links_data = update_links(links_data, old_node_name, new_node_name)
                    save_json(links_data, 'links.json')
                    
                    st.sidebar.success('Node name changed successfully!')
                    time.sleep(1)
                    st.experimental_rerun()
                else:
                    st.sidebar.warning('Please select a valid node.')
            else:
                st.sidebar.warning('Please provide a new node name.')

    # Change Node Color
    st.sidebar.subheader('Change Node Color')
    selected_node_for_color_change = st.sidebar.selectbox('Select Node', [''] + [node['id'] for node in nodes_data], key='select_node_color')
    if selected_node_for_color_change:
        node_index = next((index for index, node in enumerate(nodes_data) if node['id'] == selected_node_for_color_change), None)
        if node_index is not None:
            new_node_color = st.sidebar.color_picker('New Node Color', key=f'node_color_{node_index}')
    
            if st.sidebar.button('Change Color', key=f'change_color_button_{node_index}'):
                nodes_data[node_index]['color'] = new_node_color
                save_json(nodes_data, 'nodes.json')
                st.sidebar.success('Node color changed successfully!')
                time.sleep(1)
                st.experimental_rerun()
        else:
            st.sidebar.warning('Please select a valid node.')
    else:
        st.sidebar.warning('Please select a node to change its color.')

    # Key Management
    st.sidebar.header('Key Management')

    # Add New Key
    st.sidebar.subheader('Add New Key')
    new_key_title = st.sidebar.text_input('New Key Title')
    new_key_color = st.sidebar.color_picker('New Key Color')
    if st.sidebar.button('Add New Key'):
        if new_key_title:
            key_data.append({'title': new_key_title, 'color': new_key_color})
            st.sidebar.success('New key added successfully!')
            save_json(key_data, 'key.json')  # Save modified key data to JSON file
            time.sleep(1)
            st.experimental_rerun()
        else:
            st.sidebar.warning('Please provide a title for the new key.')

    # Edit Key Information
    st.sidebar.subheader('Edit Key Information')
    for index, key in enumerate(key_data):
        st.sidebar.write(f"Key {index + 1}: {key['title']}")
        new_title = st.sidebar.text_input(f'Title {key["title"]}', key=f'title_input_{index}', value=key['title'])
        new_color = st.sidebar.color_picker(f'Color {key["title"]}', key['color'], key=f'color_picker_{index}')
        key['title'] = new_title
        key['color'] = new_color

    # Remove Marked Keys
    st.sidebar.subheader('Key Remover')
    for index, key in enumerate(key_data):
        remove_key = st.sidebar.checkbox(f'Remove Key {index + 1}', False, key=f'remove_checkbox_{index}_{key["title"]}')
        if remove_key:
            key['marked_for_removal'] = True
    if st.sidebar.button('Remove Marked Keys'):
        # List to store indices of keys marked for removal
        keys_to_remove = []
    
        # Loop through the keys and mark those to be removed
        for index, key in enumerate(key_data):
            if key.get('marked_for_removal', False):
                keys_to_remove.append(index)
    
        # Remove marked keys from the key_data list
        for index in sorted(keys_to_remove, reverse=True):
            del key_data[index]
    
        # Save modified key data to the JSON file
        save_json(key_data, 'key.json')
    
        st.sidebar.success('Marked keys removed successfully!')
        time.sleep(1)
        st.experimental_rerun()

    # Main Content Area
    st.subheader('Node and Link Management')

    # New Node Section
    st.subheader('New Node')
    new_node_name = st.text_input('New Node Name')
    node_color = st.color_picker('Node Color')
    target_node_for_link = st.selectbox('Select Target Node for Link (Optional)', [''] + [node['id'] for node in nodes_data])
    pdf_file = st.file_uploader('Upload PDF File (Required)', type='pdf')
    pdf_uploaded = pdf_file is not None
    add_node_button = st.button('Add Node', disabled=not pdf_uploaded)
    if add_node_button:
        if not new_node_name or not pdf_file:
            st.warning('Please provide a node name and upload a PDF file.')
        else:
            new_node = {'id': new_node_name, 'color': node_color}
            nodes_data.append(new_node)
            save_json(nodes_data, 'nodes.json')
    
            pdf_dir = "pdfs"
            os.makedirs(pdf_dir, exist_ok=True)
            pdf_file_name = f"{pdf_dir}/{new_node_name.replace(' ', '_')}.pdf"
            with open(pdf_file_name, 'wb') as f:
                f.write(pdf_file.getvalue())
                
            st.success('Node added successfully!')
            
            if target_node_for_link:
                new_link = {'source': new_node_name, 'target': target_node_for_link}
                links_data.append(new_link)
                save_json(links_data, 'links.json')
                st.success('Link from the new node added successfully!')
            time.sleep(1)
            st.experimental_rerun()

    # PDF Updater
    st.subheader('PDF Updater')
    st.subheader('Update PDF for Node')
    node_to_update_pdf = st.selectbox('Select Node', [''] + [node['id'] for node in nodes_data])
    new_pdf_file = st.file_uploader('Upload New PDF File', type='pdf')
    if st.button('Update PDF'):
        if node_to_update_pdf:
            if new_pdf_file:
                pdf_file_path = update_pdf(nodes_data, node_to_update_pdf, new_pdf_file)
                st.success(f'PDF for {node_to_update_pdf} updated successfully!')
                time.sleep(1)
                st.experimental_rerun()
            else:
                st.warning('Please upload a new PDF file.')
        else:
            st.warning('Please select a node.')

    # Link Editor
    st.subheader('Create Link')
    source_node = st.selectbox('Source Node', [''] + [node['id'] for node in nodes_data])
    target_node = st.selectbox('Target Node', [''] + [node['id'] for node in nodes_data])
    if st.button('Add Link'):
        if source_node and target_node:
            if source_node != target_node:
                if not any(link['source'] == source_node and link['target'] == target_node for link in links_data):
                    new_link = {'source': source_node, 'target': target_node}
                    links_data.append(new_link)
                    save_json(links_data, 'links.json')
                    st.success('Link added successfully!')
                    time.sleep(1)
                    st.experimental_rerun()
                else:
                    st.warning('The link already exists!')
            else:
                st.warning('Source and target nodes cannot be the same!')
        else:
            st.warning('Please select both source and target nodes for the link.')

    # Link Remover
    st.subheader('Link Removal')
    selected_link = st.selectbox('Links', [''] + [f"{link['source']} -> {link['target']}" for link in links_data])
    if st.button('Remove Link'):
        if selected_link:
            index_to_remove = [f"{link['source']} -> {link['target']}" for link in links_data].index(selected_link)
            links_data = remove_link(links_data, index_to_remove)
            save_json(links_data, 'links.json')
            st.success('Link removed successfully!')
        else:
            st.warning('Please select a link to remove.')

    # Unique Colors and Hex Values
    st.subheader('Current Node Colors')
    
    # Define a function to create a colored square with the hex code
    def color_square_with_hex(color, hex_code):
        return f'<div style="display: inline-block; margin-right: 30px; vertical-align: middle; background-color: {color}; width: 40px; height: 40px;"></div> {hex_code}'
    
    unique_colors = list(set(node['color'] for node in nodes_data))
    color_hex_pairs = [(color, color) for color in unique_colors]  # Assuming color variable already contains hex code
    
    # Group color-hex pairs by twos
    pairs_grouped = [color_hex_pairs[i:i+2] for i in range(0, len(color_hex_pairs), 2)]
    
    # Display each pair of color and hex code on a line
    for pairs in pairs_grouped:
        line_html = " ".join(color_square_with_hex(pair[0], pair[1]) for pair in pairs)
        st.markdown(line_html, unsafe_allow_html=True)


    # Default theme values
    default_theme = {
        "backgroundColor": "#1E1E1E",
        "linkColor": "#2F4F4F",
        "logoImageUrl": "https://upload.wikimedia.org/wikipedia/commons/8/85/TD_SYNNEX_logo_file.png",
        "faviconUrl": "https://upload.wikimedia.org/584/commons/8/85/TD_SYNNEX_logo_file.png",
        "pageTitle": "AI Understanding",
        "textColor": "#FFFFFF",
        "controlPanelVisibility": True
    }
    
    # Streamlit app layout
    st.title("Theme Editor")
    
    st.subheader("Theme Settings")
    
    # Background Color
    background_color = st.color_picker("Background Color", value=default_theme["backgroundColor"])
    
    # Link Color
    link_color = st.color_picker("Link Color", value=default_theme["linkColor"])
    
    # Logo Image URL
    logo_image_url = st.text_input("Logo Image URL", value=default_theme["logoImageUrl"])
    
    # Favicon URL
    favicon_url = st.text_input("Favicon URL", value=default_theme["faviconUrl"])
    
    # Page Title
    page_title = st.text_input("Page Title", value=default_theme["pageTitle"])
    
    # Text Color
    text_color = st.color_picker("Text Color", value=default_theme["textColor"])
    
    # Control Panel Visibility
    control_panel_visibility = st.checkbox("Control Panel Visibility", value=default_theme["controlPanelVisibility"])
    
    # Reset to Default button
    if st.button("Reset to Default"):
        background_color = default_theme["backgroundColor"]
        link_color = default_theme["linkColor"]
        logo_image_url = default_theme["logoImageUrl"]
        favicon_url = default_theme["faviconUrl"]
        page_title = default_theme["pageTitle"]
        text_color = default_theme["textColor"]
        control_panel_visibility = default_theme["controlPanelVisibility"]
    
    # Save button
    if st.button("Save"):
        theme = {
            "backgroundColor": background_color,
            "linkColor": link_color,
            "logoImageUrl": logo_image_url,
            "faviconUrl": favicon_url,
            "pageTitle": page_title,
            "textColor": text_color,
            "controlPanelVisibility": control_panel_visibility
        }
    
        # Save theme to a JSON file
        with open("theme.json", "w") as f:
            json.dump(theme, f)
    
        st.success("Theme settings saved successfully!")


if __name__ == '__main__':
    png_path = "path1.png"
    logo = open(png_path, "rb").read()
    st.set_page_config(page_title='Mycelium', page_icon=logo) 
    main()
