-- =============================================================================
-- SMARTBUILD - ESQUEMA BASE DE DATOS (POSTGRESQL)
-- Proyecto ADSO - Ficha 3336152
-- Aprendiz: Gustavo Andrés Ortega Valencia
-- =============================================================================

-- 1. Eliminar tablas si ya existen (para reejecución limpia)
DROP TABLE IF EXISTS detalle_cotizacion CASCADE;
DROP TABLE IF EXISTS cotizaciones CASCADE;
DROP TABLE IF EXISTS reglas_compatibilidad CASCADE;
DROP TABLE IF EXISTS componentes CASCADE;
DROP TABLE IF EXISTS categoria_componente CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;

-- 2. Tabla de Usuarios
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(20) DEFAULT 'cliente' CHECK (rol IN ('cliente', 'admin')),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabla de Categorías de Componentes (CPU, GPU, RAM, Motherboard, PSU, etc.)
CREATE TABLE categoria_componente (
    id_categoria SERIAL PRIMARY KEY,
    nombre_categoria VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT
);

-- 4. Tabla de Catálogo de Componentes
CREATE TABLE componentes (
    id_componente SERIAL PRIMARY KEY,
    id_categoria INT REFERENCES categoria_componente(id_categoria) ON DELETE CASCADE,
    nombre VARCHAR(150) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    precio NUMERIC(12, 2) NOT NULL CHECK (precio >= 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    consumo_tdp_watts INT DEFAULT 0 CHECK (consumo_tdp_watts >= 0),
    especificaciones JSONB DEFAULT '{}'::jsonb, -- Datos específicos dinámicos
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tabla de Reglas Técnicas de Compatibilidad de Hardware
CREATE TABLE reglas_compatibilidad (
    id_regla SERIAL PRIMARY KEY,
    socket_cpu VARCHAR(30),             -- Ej: 'AM4', 'AM5', 'LGA1700'
    factor_forma VARCHAR(30),           -- Ej: 'ATX', 'Micro-ATX', 'ITX'
    tipo_memoria_ram VARCHAR(20),       -- Ej: 'DDR4', 'DDR5'
    frecuencia_ram_max_mhz INT CHECK (frecuencia_ram_max_mhz BETWEEN 2133 AND 8000),
    potencia_fuente_recomendada_watts INT CHECK (potencia_fuente_recomendada_watts >= 0),
    largo_gpu_max_mm INT CHECK (largo_gpu_max_mm >= 0)
);

-- 6. Tabla de Cotizaciones creadas por Usuarios
CREATE TABLE cotizaciones (
    id_cotizacion SERIAL PRIMARY KEY,
    id_usuario INT REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    nombre_cotizacion VARCHAR(100) NOT NULL DEFAULT 'Mi Configuración PC',
    precio_total NUMERIC(12, 2) DEFAULT 0.00,
    consumo_total_watts INT DEFAULT 0,
    es_compatible BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Detalle de Componentes por Cotización (Muchos a Muchos)
CREATE TABLE detalle_cotizacion (
    id_detalle SERIAL PRIMARY KEY,
    id_cotizacion INT REFERENCES cotizaciones(id_cotizacion) ON DELETE CASCADE,
    id_componente INT REFERENCES componentes(id_componente) ON DELETE CASCADE,
    cantidad INT DEFAULT 1 CHECK (cantidad > 0)
);

-- 8. Índices GIN para optimizar búsquedas JSONB en especificaciones
CREATE INDEX idx_componentes_especificaciones ON componentes USING GIN (especificaciones);