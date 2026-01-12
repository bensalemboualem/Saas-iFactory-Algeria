/**
 * CountrySelector - Sélecteur de pays DZ/CH/GLOBAL
 * =================================================
 * Composant pour sélectionner le pays cible du RAG
 */

import React from "react";
import type { CountrySelectorProps, Country } from "./types";
import { COUNTRY_OPTIONS } from "./types";

export const CountrySelector: React.FC<CountrySelectorProps> = ({
  value,
  selectedCountry,
  onChange,
  onCountryChange,
  disabled = false,
  size = "md",
  showFlags = true,
  className = "",
}) => {
  // Support both naming conventions
  const currentValue = value ?? selectedCountry ?? "DZ";
  const handleChange = onChange ?? onCountryChange ?? (() => {});

  const sizeClasses = {
    sm: "text-xs px-2 py-1",
    md: "text-sm px-3 py-2",
    lg: "text-base px-4 py-3",
  };

  return (
    <div className={`flex items-center gap-1 ${className}`}>
      {COUNTRY_OPTIONS.map((option) => (
        <button
          key={option.value}
          onClick={() => handleChange(option.value)}
          disabled={disabled}
          className={`${sizeClasses[size]} rounded-lg font-medium transition-all duration-200 flex items-center gap-1.5 ${disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer"} focus:outline-none`}
          style={{
            background: currentValue === option.value ? 'var(--iaf-green)' : 'var(--bg)',
            color: currentValue === option.value ? '#ffffff' : 'var(--iaf-text-secondary)',
            boxShadow: currentValue === option.value ? '0 0 0 2px rgba(0, 166, 81, 0.3)' : 'none',
          }}
          title={option.label}
          aria-pressed={currentValue === option.value}
        >
          {showFlags && <span className="text-lg">{option.emoji}</span>}
          <span className="hidden sm:inline">{option.label}</span>
          <span className="sm:hidden">{option.value}</span>
        </button>
      ))}
    </div>
  );
};

/**
 * Version dropdown du sélecteur
 */
export const CountrySelectorDropdown: React.FC<CountrySelectorProps> = ({
  value,
  selectedCountry,
  onChange,
  onCountryChange,
  disabled = false,
  size = "md",
  showFlags = true,
  className = "",
}) => {
  // Support both naming conventions
  const currentValue = value ?? selectedCountry ?? "DZ";
  const handleChange = onChange ?? onCountryChange ?? (() => {});

  const sizeClasses = {
    sm: "text-xs px-2 py-1",
    md: "text-sm px-3 py-2",
    lg: "text-base px-4 py-3",
  };

  return (
    <div className={`relative ${className}`}>
      <select
        value={currentValue}
        onChange={(e) => handleChange(e.target.value as Country)}
        disabled={disabled}
        className={`${sizeClasses[size]} appearance-none w-full rounded-lg focus:outline-none ${disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer"} pr-10`}
        style={{
          background: 'var(--card)',
          border: '1px solid var(--border)',
          color: 'var(--text)',
        }}
      >
        {COUNTRY_OPTIONS.map((option) => (
          <option key={option.value} value={option.value}>
            {showFlags ? `${option.emoji} ` : ""}
            {option.label}
          </option>
        ))}
      </select>

      {/* Dropdown arrow */}
      <div className="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
        <svg
          className="h-5 w-5"
          style={{ color: 'var(--iaf-text-secondary)' }}
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fillRule="evenodd"
            d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
            clipRule="evenodd"
          />
        </svg>
      </div>
    </div>
  );
};

export default CountrySelector;
