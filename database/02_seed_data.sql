-- =============================================================================
-- SMARTBUILD - DATOS DE PRUEBA INICIALES (POSTGRESQL SEED)
-- Proyecto ADSO - Ficha 3336152
-- Aprendiz: Gustavo Andrés Ortega Valencia
-- =============================================================================

-- 1. Insertar Categorías Principales
INSERT INTO categoria_componente (id_categoria, nombre_categoria, descripcion) VALUES
(1, 'Procesador (CPU)', 'Unidad Central de Procesamiento'),
(2, 'Tarjeta Madre (Motherboard)', 'Placa principal del sistema'),
(3, 'Memoria RAM', 'Memoria de acceso aleatorio'),
(4, 'Tarjeta de Video (GPU)', 'Unidad de procesamiento gráfico'),
(5, 'Fuente de Poder (PSU)', 'Suministro de energía eléctrica'),
(6, 'Almacenamiento', 'Discos de estado sólido SSD NVMe / SATA');

-- 2. Insertar Usuarios de Prueba (Administrador y Cliente)
INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES
('Gustavo Ortega', 'gustavo@smartbuild.com', 'scrypt:32768:8:1$hash_admin_secret', 'admin'),
('Usuario Demo', 'cliente@gmail.com', 'scrypt:32768:8:1$hash_cliente_secret', 'cliente');

-- 3. Insertar Componentes Reales de Hardware
-- Procesadores
INSERT INTO componentes (id_categoria, nombre, marca, modelo, precio, stock, consumo_tdp_watts, especificaciones) VALUES
(1, 'AMD Ryzen 5 7600X', 'AMD', '100-100000593WOF', 980000.00, 10, 105, '{"socket": "AM5", "nucleos": 6, "hilos": 12, "frecuencia_base_ghz": 4.7, "graficos_integrados": true}'::jsonb),
(1, 'Intel Core i5-13400F', 'Intel', 'BX8071513400F', 850000.00, 8, 65, '{"socket": "LGA1700", "nucleos": 10, "hilos": 16, "frecuencia_base_ghz": 2.5, "graficos_integrados": false}'::jsonb);

-- Tarjetas Madre
INSERT INTO componentes (id_categoria, nombre, marca, modelo, precio, stock, consumo_tdp_watts, especificaciones) VALUES
(2, 'ASUS TUF Gaming B650-PLUS WiFi', 'ASUS', 'B650-PLUS', 920000.00, 5, 30, '{"socket": "AM5", "factor_forma": "ATX", "tipo_ram": "DDR5", "ranuras_ram": 4, "frecuencia_max_ram_mhz": 6400}'::jsonb),
(2, 'MSI PRO B760M-A WiFi', 'MSI', 'B760M-A', 680000.00, 6, 25, '{"socket": "LGA1700", "factor_forma": "Micro-ATX", "tipo_ram": "DDR4", "ranuras_ram": 4, "frecuencia_max_ram_mhz": 5333}'::jsonb);

-- Memoria RAM
INSERT INTO componentes (id_categoria, nombre, marca, modelo, precio, stock, consumo_tdp_watts, especificaciones) VALUES
(3, 'Kingston Fury Beast DDR5 32GB (2x16GB) 6000MHz', 'Kingston', 'KF560C36BBEK2-32', 540000.00, 15, 10, '{"tipo_ram": "DDR5", "capacidad_gb": 32, "frecuencia_mhz": 6000, "latencia_cl": 36}'::jsonb),
(3, 'Corsair Vengeance LPX DDR4 16GB (2x8GB) 3200MHz', 'Corsair', 'CMK16GX4M2E3200C16', 210000.00, 20, 5, '{"tipo_ram": "DDR4", "capacidad_gb": 16, "frecuencia_mhz": 3200, "latencia_cl": 16}'::jsonb);

-- Tarjetas de Video
INSERT INTO componentes (id_categoria, nombre, marca, modelo, precio, stock, consumo_tdp_watts, especificaciones) VALUES
(4, 'Nvidia GeForce RTX 4060 8GB', 'Gigabyte', 'GV-N4060EAGLE OC-8GD', 1450000.00, 7, 115, '{"vram_gb": 8, "tipo_vram": "GDDR6", "largo_mm": 272, "puerto_pcie": "PCIe 4.0 x8"}'::jsonb),
(4, 'AMD Radeon RX 6600 8GB', 'PowerColor', 'AXRX 6600 8GBD6-3DH', 990000.00, 12, 132, '{"vram_gb": 8, "tipo_vram": "GDDR6", "largo_mm": 200, "puerto_pcie": "PCIe 4.0 x8"}'::jsonb);

-- Fuentes de Poder
INSERT INTO componentes (id_categoria, nombre, marca, modelo, precio, stock, consumo_tdp_watts, especificaciones) VALUES
(5, 'Corsair RM750e 750W 80 Plus Gold', 'Corsair', 'CP-9020262-NA', 510000.00, 10, 0, '{"potencia_watts": 750, "certificacion": "80 Plus Gold", "modular": true}'::jsonb),
(5, 'EVGA 600 W1 600W 80 Plus White', 'EVGA', '100-W1-0600-K1', 230000.00, 14, 0, '{"potencia_watts": 600, "certificacion": "80 Plus White", "modular": false}'::jsonb);

-- Almacenamiento
INSERT INTO componentes (id_categoria, nombre, marca, modelo, precio, stock, consumo_tdp_watts, especificaciones) VALUES
(6, 'SSD NVMe Kingston KC3000 1TB PCIe 4.0', 'Kingston', 'SKC3000S/1024G', 380000.00, 18, 7, '{"capacidad_gb": 1024, "tipo_interface": "M.2 NVMe PCIe 4.0", "lectura_mb_s": 7000}'::jsonb);