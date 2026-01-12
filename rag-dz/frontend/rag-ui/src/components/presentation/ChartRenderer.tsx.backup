/**
 * Rendu des graphiques simples en SVG pur
 * Sans dépendances externes (recharts serait mieux mais pour commencer)
 */

import React from 'react';
import type { ChartData } from './types';

export const ChartRenderer: React.FC<{ chart: ChartData }> = ({ chart }) => {
  const height = chart.config?.height || 300;
  const colors = chart.config?.colors || ['#006233', '#D21034', '#3B82F6', '#10B981', '#F59E0B'];

  if (chart.type === 'bar') {
    return <BarChart chart={chart} height={height} colors={colors} />;
  }

  if (chart.type === 'comparison') {
    return <ComparisonChart chart={chart} height={height} />;
  }

  if (chart.type === 'pie') {
    return <PieChart chart={chart} height={height} colors={colors} />;
  }

  return (
    <div className="chart-container">
      <h3>{chart.title}</h3>
      <p className="chart-placeholder">Type de graphique: {chart.type}</p>
    </div>
  );
};

// Bar Chart simple
const BarChart: React.FC<{ chart: ChartData; height: number; colors: string[] }> = ({
  chart,
  height,
  colors
}) => {
  const data = chart.data;
  const maxValue = Math.max(...data.map(d => d.value || 0));
  const barWidth = 60;
  const spacing = 20;
  const width = data.length * (barWidth + spacing) + 60;

  return (
    <div className="chart-container">
      <h3>{chart.title}</h3>
      <svg width={width} height={height} className="chart-svg">
        {/* Y-axis */}
        <line x1="40" y1="20" x2="40" y2={height - 40} stroke="#666" strokeWidth="2" />
        {/* X-axis */}
        <line x1="40" y1={height - 40} x2={width - 20} y2={height - 40} stroke="#666" strokeWidth="2" />

        {/* Bars */}
        {data.map((item, index) => {
          const barHeight = ((item.value || 0) / maxValue) * (height - 80);
          const x = 50 + index * (barWidth + spacing);
          const y = height - 40 - barHeight;

          return (
            <g key={index}>
              <rect
                x={x}
                y={y}
                width={barWidth}
                height={barHeight}
                fill={colors[index % colors.length]}
                opacity="0.8"
              />
              <text
                x={x + barWidth / 2}
                y={height - 20}
                textAnchor="middle"
                fontSize="12"
                fill="#fff"
              >
                {item.name}
              </text>
              <text
                x={x + barWidth / 2}
                y={y - 5}
                textAnchor="middle"
                fontSize="11"
                fill="#fff"
              >
                {item.value}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};

// Comparison Chart (Algérie vs Suisse)
const ComparisonChart: React.FC<{ chart: ChartData; height: number }> = ({
  chart,
  height
}) => {
  const data = chart.data;
  const maxValue = Math.max(
    ...data.flatMap(d => [d.algerie || 0, d.suisse || 0])
  );
  const barHeight = 30;
  const spacing = 15;
  const width = 600;

  return (
    <div className="chart-container comparison">
      <h3>{chart.title}</h3>
      <svg width={width} height={data.length * (barHeight * 2 + spacing) + 60} className="chart-svg">
        {data.map((item, index) => {
          const y = 30 + index * (barHeight * 2 + spacing);
          const dzWidth = ((item.algerie || 0) / maxValue) * 350;
          const chWidth = ((item.suisse || 0) / maxValue) * 350;

          return (
            <g key={index}>
              {/* Criterion label */}
              <text x="10" y={y + 15} fontSize="12" fill="#fff">
                {item.criterion}
              </text>

              {/* Algeria bar */}
              <rect
                x="200"
                y={y}
                width={dzWidth}
                height={barHeight}
                fill="#006233"
                opacity="0.8"
              />
              <text
                x={210 + dzWidth}
                y={y + 20}
                fontSize="11"
                fill="#fff"
              >
                🇩🇿 {item.algerie}
              </text>

              {/* Switzerland bar */}
              <rect
                x="200"
                y={y + barHeight + 5}
                width={chWidth}
                height={barHeight}
                fill="#FF0000"
                opacity="0.8"
              />
              <text
                x={210 + chWidth}
                y={y + barHeight + 25}
                fontSize="11"
                fill="#fff"
              >
                🇨🇭 {item.suisse}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};

// Pie Chart simple
const PieChart: React.FC<{ chart: ChartData; height: number; colors: string[] }> = ({
  chart,
  height,
  colors
}) => {
  const data = chart.data;
  const total = data.reduce((sum, item) => sum + (item.value || 0), 0);
  const centerX = height / 2;
  const centerY = height / 2;
  const radius = (height / 2) - 40;

  let currentAngle = 0;

  return (
    <div className="chart-container">
      <h3>{chart.title}</h3>
      <svg width={height} height={height} className="chart-svg">
        {data.map((item, index) => {
          const percentage = (item.value || 0) / total;
          const angle = percentage * 2 * Math.PI;

          const x1 = centerX + radius * Math.cos(currentAngle - Math.PI / 2);
          const y1 = centerY + radius * Math.sin(currentAngle - Math.PI / 2);
          const x2 = centerX + radius * Math.cos(currentAngle + angle - Math.PI / 2);
          const y2 = centerY + radius * Math.sin(currentAngle + angle - Math.PI / 2);

          const largeArc = angle > Math.PI ? 1 : 0;

          const pathData = [
            `M ${centerX} ${centerY}`,
            `L ${x1} ${y1}`,
            `A ${radius} ${radius} 0 ${largeArc} 1 ${x2} ${y2}`,
            'Z'
          ].join(' ');

          const labelAngle = currentAngle + angle / 2;
          const labelX = centerX + (radius * 0.7) * Math.cos(labelAngle - Math.PI / 2);
          const labelY = centerY + (radius * 0.7) * Math.sin(labelAngle - Math.PI / 2);

          currentAngle += angle;

          return (
            <g key={index}>
              <path
                d={pathData}
                fill={colors[index % colors.length]}
                opacity="0.8"
                stroke="#fff"
                strokeWidth="2"
              />
              <text
                x={labelX}
                y={labelY}
                textAnchor="middle"
                fontSize="11"
                fill="#fff"
                fontWeight="bold"
              >
                {Math.round(percentage * 100)}%
              </text>
            </g>
          );
        })}

        {/* Legend */}
        {data.map((item, index) => (
          <g key={`legend-${index}`}>
            <rect
              x={height + 10}
              y={20 + index * 25}
              width="15"
              height="15"
              fill={colors[index % colors.length]}
            />
            <text
              x={height + 30}
              y={32 + index * 25}
              fontSize="12"
              fill="#fff"
            >
              {item.name}
            </text>
          </g>
        ))}
      </svg>
    </div>
  );
};
