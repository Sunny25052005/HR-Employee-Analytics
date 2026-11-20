-- =============================================================================
-- Script 01: Database Creation
-- Project: HR Employee Analytics Dashboard
-- Database Engine: MySQL 8.0+
-- Description: Creates the dedicated hr_analytics schema with utf8mb4 encoding.
-- =============================================================================

-- Drop database if it exists (for clean staging / automated CI pipelines)
-- DROP DATABASE IF EXISTS hr_analytics;

-- Create Database with proper Unicode collation
CREATE DATABASE IF NOT EXISTS hr_analytics
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Verify database creation
SHOW DATABASES LIKE 'hr_analytics';

-- Switch context to hr_analytics
USE hr_analytics;
