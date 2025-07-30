ROLES = (
    ('cliente', 'Cliente'),
    ('asesor', 'Asesor'),
    ('supervisor', 'Supervisor'),
    ('tecnico', 'Técnico'),
    ('codificador', 'Codificador'),
    ('admin', 'Administrador'),
)

PERMISOS_ROL = {
    'cliente': ['view_own_orders', 'view_own_vehicles'],
    'asesor': ['manage_orders', 'view_customers', 'create_budgets'],
    'supervisor': ['view_all_orders', 'manage_team', 'approve_budgets'],
    'tecnico': ['update_work_orders', 'manage_inventory'],
    'codificador': ['manage_parts_catalog', 'update_inventory'],
    'admin': ['all_permissions']
}
