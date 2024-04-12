import streamlit as st
import json

# Read nodes data from JSON file
with open("nodes.json", "r") as f:
    nodes_content = f.read()
    nodes = json.loads(nodes_content)

# Read links data from JSON file
with open("links.json", "r") as f:
    links_content = f.read()
    links = json.loads(links_content)

# Custom HTML/CSS/JS code for draggable nodes using D3.js
custom_html = """
<!DOCTYPE html>
<html>
<head>
  <title>Interactive Graph</title>
  <script src="https://d3js.org/d3.v5.min.js"></script>
  <style>
    body, html {
        height: 100%;
        margin: 0;
        overflow: hidden;
        background-color: #1E1E1E; /* Set dark background color */
        color: #FFFFFF; /* Set text color to white */
    }

    .graph-container {
        width: 100%;
        height: 100%;
        cursor: grab;
    }

    .node {
      cursor: pointer;
    }

    .node circle {
      stroke: #000;
      stroke-width: 1.5px;
    }

    .node text {
      font-size: 12px;
      text-anchor: middle;
    }

    .link {
      stroke: black;
      stroke-width: 2px;
    }

    .search-container {
      position: absolute;
      top: 10px;
      right: 10px;
      z-index: 9999;
    }

    .node:hover .hover-circle {
      display: block;
    }

    .hover-circle {
      display: none;
    }
  </style>
</head>
<body>
  <div class="search-container">
    <input list="nodes" type="text" id="searchInput" placeholder="Search node...">
    <datalist id="nodes">
      <!-- Suggestions will be populated here dynamically -->
    </datalist>
    <button id="button">Go</button>
  </div>

  <div class="graph-container">
    <svg width="100%" height="100%">
      <g id="container"></g>
    </svg>
  </div>

  <script>
var width = window.innerWidth,
    height = window.innerHeight;

var svg = d3.select("svg"),
    container = d3.select("#container"),
    nodes = """ + json.dumps(nodes) + """,
    links = """ + json.dumps(links) + """,
    radius = 10;

var simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(function(d) { return d.id; }).distance(200))
    .force("charge", d3.forceManyBody().strength(-1000))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .on("tick", ticked);

var link = container.selectAll(".link")
    .data(links)
    .enter().append("line")
    .attr("class", "link")
    .style("stroke", "gray")
    .style("stroke-width", "2px");

var node = container.selectAll(".node")
    .data(nodes)
    .enter().append("g")
    .attr("class", "node")
    .call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended))
    .on("mouseover", function(d) {
        d3.select(this).select("circle").attr("fill", d.color); // Change node color on hover
        d3.selectAll(".link")
          .filter(function(l) { return l.source === d || l.target === d; })
          .style("stroke", d.color); // Change link color on hover
        d3.select(this).select(".hover-circle").style("display", "block");
        d3.select(this).select("button").transition().duration(300).style("opacity", 1); // Fade in button
    })
    .on("mouseout", function(d) {
        d3.select(this).select("circle").attr("fill", function(d) { return d.color; }); // Revert node color
        d3.selectAll(".link").style("stroke", "gray"); // Revert link color
        d3.select(this).select(".hover-circle").style("display", "none");
        d3.select(this).select("button").transition().duration(300).style("opacity", 0); // Fade out button
    });

node.append("circle")
    .attr("r", radius)
    .attr("fill", function(d) { return d.color; });

node.append("text")
    .attr("dx", 0)
    .attr("dy", -radius - 5)
    .attr("text-anchor", "middle")
    .attr("fill", "white")
    .text(function(d) { return d.id; });

node.append("circle")
    .attr("class", "hover-circle")
    .attr("r", radius / 2)
    .attr("fill", "red")
    .attr("stroke", "black")
    .attr("stroke-width", "2px")
    .on("click", function(d) {
        var filename = d.id.replace(/\\s+/g, '_') + ".pdf";
        window.open("http://brig.digital:8501/pdfs/" + filename, "_blank");
        d3.event.stopPropagation(); // Stop propagation of the click event
    });

node.append("button")
    .text("Click me")
    .style("opacity", 0) // Initially hide button
    .style("background-color", "red") // Set button color to red
    .on("click", function(d) {
        var filename = d.id.replace(/\\s+/g, '_') + ".pdf";
        window.open("http://brig.digital:8501/pdfs/" + filename, "_blank");
        d3.event.stopPropagation(); // Stop propagation of the click event
    });

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

restart();

function restart() {
  link = link.data(links);
  link.enter().append("line")
      .attr("class", "link")
      .style("stroke", "black")
      .style("stroke-width", "2px")
      .merge(link);

  simulation.nodes(nodes);
  simulation.force("link").links(links);
  simulation.alpha(1).restart();
}

function ticked() {
  link.attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

  node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
}

function searchNode() {
  var selectedVal = document.getElementById('searchInput').value;
  var selectedNode = nodes.find(function(d) { return d.id === selectedVal; });
  if (selectedNode) {
    // Calculate the offset to center the selected node
    var offsetX = width / 1.839 - selectedNode.x;
    var offsetY = height / 3.95 - selectedNode.y;
    // Apply transition to zoom to the selected node
    svg.transition()
      .duration(750)
      .call(zoom.transform, d3.zoomIdentity.translate(offsetX, offsetY).scale(1));
  }
}

var zoom = d3.zoom()
    .on("zoom", function () {
      container.attr("transform", d3.event.transform);
    });

svg.call(zoom);

// Populate suggestions
var suggestions = nodes.map(function(node) { return node.id; });
var datalist = d3.select("#nodes");
datalist.selectAll("option")
  .data(suggestions)
  .enter().append("option")
  .attr("value", function(d) { return d; });

// Handle Enter key for search
document.getElementById("searchInput").addEventListener("keyup", function(event) {
  if (event.key === "Enter") {
    searchNode();
  }
});

  </script>
</body>
</html>
"""

def main():
    st.set_page_config(layout="wide")  # Set the page layout to wide
    st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)
    st.markdown(" <style> div[class^='css-1544g2n'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)
    # Display custom HTML/CSS/JS
    st.components.v1.html(custom_html, height=1400)

if __name__ == "__main__":
    main()
