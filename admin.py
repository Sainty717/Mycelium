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

# Streamlit app
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
    #st.beta_set_page_config(page_title='Mycelium', page_icon=logo) 
    #st.set_page_config(page_title="Stock Price", page_icon=logo, layout="centered", initial_sidebar_state = "auto")
   
    # Sidebar panel
    st.sidebar.header('Node and Link Removal')
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

    # Node editor
    st.header('New Node')
    new_node_name = st.text_input('New Node Name')
    node_color = st.color_picker('Node Color')
    
    # Select target node for the link from the new node
    target_node_for_link = st.selectbox('Select Target Node for Link (Optional)', [''] + [node['id'] for node in nodes_data])
    
    pdf_file = st.file_uploader('Upload PDF File (Required)', type='pdf')

    # Boolean variable to track PDF upload
    pdf_uploaded = pdf_file is not None

    # Add Node button availability based on PDF upload
    add_node_button = st.button('Add Node', disabled=not pdf_uploaded)

    if add_node_button:
        if not new_node_name or not pdf_file:
            st.warning('Please provide a node name and upload a PDF file.')
        else:
            new_node = {'id': new_node_name, 'color': node_color}
            nodes_data.append(new_node)
            save_json(nodes_data, 'nodes.json')
    
            # Ensure directory exists before saving PDF file
            pdf_dir = "pdfs"
            os.makedirs(pdf_dir, exist_ok=True)
    
            pdf_file_name = f"{pdf_dir}/{new_node_name.replace(' ', '_')}.pdf"
            with open(pdf_file_name, 'wb') as f:
                f.write(pdf_file.getvalue())
                
            st.success('Node added successfully!')
            
            # Add link if a target node for the link is selected
            if target_node_for_link:
                new_link = {'source': new_node_name, 'target': target_node_for_link}
                links_data.append(new_link)
                save_json(links_data, 'links.json')
                st.success('Link from the new node added successfully!')
            time.sleep(1)
            st.experimental_rerun()

    # PDF updater
    st.header('PDF Updater')
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

    # Link editor
    st.sidebar.header('Create Link')
    source_node = st.sidebar.selectbox('Source Node', [''] + [node['id'] for node in nodes_data])
    target_node = st.sidebar.selectbox('Target Node', [''] + [node['id'] for node in nodes_data])
    if st.sidebar.button('Add Link'):
        if source_node and target_node:
            # Check if the source node and target node are different
            if source_node != target_node:
                # Check if the link doesn't already exist
                if not any(link['source'] == source_node and link['target'] == target_node for link in links_data):
                    new_link = {'source': source_node, 'target': target_node}
                    links_data.append(new_link)
                    save_json(links_data, 'links.json')
                    st.sidebar.success('Link added successfully!')
                    time.sleep(1)
                    st.experimental_rerun()
                else:
                    st.sidebar.warning('The link already exists!')
            else:
                st.sidebar.warning('Source and target nodes cannot be the same!')
        else:
            st.sidebar.warning('Please select both source and target nodes for the link.')


    # Link remover
    st.sidebar.header('Link Removal')
    selected_link = st.sidebar.selectbox('Links', [''] + [f"{link['source']} -> {link['target']}" for link in links_data])

    if st.sidebar.button('Remove Link'):
        if selected_link:
            index_to_remove = [f"{link['source']} -> {link['target']}" for link in links_data].index(selected_link)
            links_data = remove_link(links_data, index_to_remove)
            save_json(links_data, 'links.json')
            st.sidebar.success('Link removed successfully!')
        else:
            st.sidebar.warning('Please select a link to remove.')


    
    # Node color changer
    st.sidebar.header('Change Node Color')
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


if __name__ == '__main__':
    png_path = "path1.png"
    logo = open(png_path, "rb").read()
    st.set_page_config(page_title='Mycelium', page_icon=logo) 
    main()
