-- Script d'initialisation de la base de données Gateway
-- =====================================================

-- Créer la base de données si elle n'existe pas
CREATE DATABASE iafactory_gateway;

-- Se connecter à la base de données
\c iafactory_gateway;

-- Créer un utilisateur avec les bons droits
CREATE USER iafactory WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE iafactory_gateway TO iafactory;
GRANT ALL ON SCHEMA public TO iafactory;

-- Afficher un message de succès
SELECT 'Base de données iafactory_gateway créée avec succès!' as message;
