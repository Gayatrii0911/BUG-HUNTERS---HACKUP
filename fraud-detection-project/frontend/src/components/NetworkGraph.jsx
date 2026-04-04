import React, { useEffect, useRef } from 'react';
import cytoscape from 'cytoscape';

const NetworkGraph = ({ data, onNodeClick, highlightNode }) => {
  const containerRef = useRef(null);
  const cyRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current || !data) return;

    // Destroy existing instance
    if (cyRef.current) {
      cyRef.current.destroy();
    }

    const cy = cytoscape({
      container: containerRef.current,
      elements: data,
      boxSelectionEnabled: false,
      autounselectify: true,
      style: [
        {
          selector: 'node',
          style: {
            'background-color': '#1a1c2e',
            'border-width': 2,
            'border-color': '#00f5ff',
            'label': 'data(label)',
            'color': '#cbd5e0',
            'font-family': 'JetBrains Mono',
            'font-size': '8px',
            'width': '35px',
            'height': '35px',
            'text-valign': 'bottom',
            'text-margin-y': '5px',
            'overlay-opacity': 0,
            'transition-property': 'background-color, border-color, border-width, box-shadow',
            'transition-duration': '0.3s'
          }
        },
        {
          selector: 'node[?is_fraudulent]',
          style: {
            'background-color': '#ef4444',
            'border-color': '#ef4444',
            'color': '#ef4444',
            'shadow-blur': 15,
            'shadow-color': '#ef4444',
            'shadow-opacity': 0.8
          }
        },
        {
          selector: 'node[?is_moderate_risk]',
          style: {
            'background-color': '#f59e0b',
            'border-color': '#f59e0b'
          }
        },
        {
          selector: 'node[?is_blocked]',
          style: {
             'border-style': 'double',
             'border-width': 5,
             'opacity': 0.8,
             'content': (ele) => `${ele.data('id')} [ LOCKED ]`,
             'color': '#ef4444'
          }
        },
        {
          // HIGHLIGHT TARGET: High-visibility investigative focus
          selector: `node[id = "${highlightNode}"]`,
          style: {
            'border-color': '#39ff14',
            'border-width': 10,
            'shadow-blur': 40,
            'shadow-color': '#39ff14',
            'shadow-opacity': 1,
            'width': '55px',
            'height': '55px',
            'z-index': 9999
          }
        },
        {
          selector: 'node:selected',
          style: {
            'border-color': '#bc13fe',
            'border-width': 4
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 1.5,
            'line-color': 'rgba(0, 245, 255, 0.2)',
            'target-arrow-color': 'rgba(0, 245, 255, 0.2)',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'label': 'data(amount)',
            'font-size': '6px',
            'color': '#4a5568',
            'text-rotation': 'autorotate',
            'text-margin-y': '-10px'
          }
        },
        {
          selector: 'edge[decision = "APPROVE"]',
          style: {
            'line-color': 'rgba(0, 245, 255, 0.4)',
            'target-arrow-color': 'rgba(0, 245, 255, 0.4)',
            'width': 1.5,
            'label': (ele) => `${ele.data('decision')}: ₹${ele.data('amount')}`,
            'font-size': '7px',
            'color': '#00f5ff',
            'text-background-color': '#080a12',
            'text-background-opacity': 1,
            'text-background-padding': '1px'
          }
        },
        {
          selector: 'edge[decision = "MFA"]',
          style: {
            'line-color': '#f59e0b',
            'target-arrow-color': '#f59e0b',
            'width': 2.5,
            'line-style': 'dashed',
            'label': (ele) => `${ele.data('decision')}: ₹${ele.data('amount')}`,
            'font-size': '8px',
            'color': '#f59e0b',
            'text-background-color': '#080a12',
            'text-background-opacity': 1
          }
        },
        {
          selector: 'edge[?is_suspicious]',
          style: {
            'line-color': '#ffcc00',
            'target-arrow-color': '#ffcc00',
            'width': 2.5,
            'label': (ele) => `₹${ele.data('amount')}`
          }
        },
        {
          selector: 'edge[?is_fraud]',
          style: {
            'line-color': '#ff003c',
            'target-arrow-color': '#ff003c',
            'width': 4,
            'line-style': 'solid',
            'opacity': 1,
            'overlay-color': '#ff003c',
            'overlay-padding': 3,
            'overlay-opacity': 0.2,
            'label': (ele) => `${ele.data('decision')}: ₹${ele.data('amount')}`
          }
        },
        {
          selector: 'edge[?is_blocked]',
          style: {
            'line-color': '#475569',
            'target-arrow-color': '#475569',
            'width': 2,
            'line-style': 'dashed',
            'line-dash-pattern': [6, 3],
            'opacity': 0.4,
            'label': (ele) => `BLOCKED: ₹${ele.data('amount')}`,
            'color': '#ef4444',
            'font-size': '8px',
            'font-weight': 'bold',
            'text-background-color': '#080a12',
            'text-background-opacity': 1,
            'text-background-padding': '2px'
          }
        }
      ],
      layout: {
        name: 'cose',
        animate: true,
        randomize: true,
        componentSpacing: 150,
        nodeRepulsion: 8000,
        edgeElasticity: 100,
        nestingFactor: 5,
        gravity: 80,
        numIter: 1000,
        initialTemp: 200,
        coolingFactor: 0.95,
        minTemp: 1.0
      }
    });

    cy.on('tap', 'node', (evt) => {
      onNodeClick(evt.target.data());
    });

    // Add interactivity: hover effect
    cy.on('mouseover', 'node', (e) => {
       e.target.style({
         'border-width': 5,
         'border-color': '#bc13fe'
       });
       document.body.style.cursor = 'pointer';
    });
    
    cy.on('mouseout', 'node', (e) => {
       e.target.removeStyle();
       document.body.style.cursor = 'default';
    });

    cyRef.current = cy;

    // Ensure the graph fits and recalculates layout on data change
    if (data && data.length > 0) {
      cy.layout({
        name: 'cose',
        animate: true,
        fit: true,
        padding: 50,
        randomize: false,
        componentSpacing: 100,
        nodeRepulsion: 4000,
        edgeElasticity: 100
      }).run();
      cy.resize();
      cy.fit();
    }
    
    return () => {
      if (cyRef.current) {
        cyRef.current.destroy();
      }
    };
  }, [data]);

  return <div ref={containerRef} className="w-full h-full" />;
};

export default NetworkGraph;
