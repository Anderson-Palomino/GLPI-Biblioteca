-- ============================================================
-- GLPI - Sistema de Gestión Bibliotecaria
-- Script de datos de ejemplo
-- Ejecutar DESPUÉS de completar la instalación web de GLPI
-- ============================================================

USE glpi;

-- ============================================================
-- CATEGORÍAS DE LIBROS (como categorías de activos)
-- ============================================================
INSERT INTO glpi_itilcategories (name, completename, comment, level, entities_id, is_recursive)
VALUES
  ('Literatura', 'Literatura', 'Novelas, cuentos, poesía', 1, 0, 1),
  ('Ciencias', 'Ciencias', 'Física, Química, Biología, Matemáticas', 1, 0, 1),
  ('Historia', 'Historia', 'Historia universal, peruana, geografía', 1, 0, 1),
  ('Tecnología', 'Tecnología', 'Informática, ingeniería, programación', 1, 0, 1),
  ('Arte', 'Arte', 'Pintura, música, arquitectura, diseño', 1, 0, 1)
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- ============================================================
-- NOTA: Los libros se crean como "Computers" o tipo de activo
-- personalizado via interfaz web. Ver guía SETUP.md
-- ============================================================

-- Verificar datos cargados
SELECT 'Categorías creadas:' as info, COUNT(*) as total FROM glpi_itilcategories WHERE name IN ('Literatura','Ciencias','Historia','Tecnología','Arte');
