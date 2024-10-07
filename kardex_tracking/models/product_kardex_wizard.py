from odoo import models, fields, api

class ProductKardexWizard(models.TransientModel):
    _name = 'product.kardex.wizard'
    _description = 'Product Kardex Wizard'

    product_id = fields.Many2one('product.product', string='Producto', required=True)
    date_start = fields.Datetime(string='Fecha de Inicio', required=True)
    date_end = fields.Datetime(string='Fecha de Fin', required=True)
    remaining_qty = fields.Float(string='Cantidad Restante', compute='_compute_remaining_qty', store=False)

    @api.depends('product_id', 'date_start', 'date_end')
    def _compute_remaining_qty(self):
        for wizard in self:
            stock_moves = self.env['stock.move'].search([
                ('product_id', '=', wizard.product_id.id),
                ('date', '<=', wizard.date_end),
                ('state', '=', 'done')
            ])
            in_qty = sum(move.product_uom_qty for move in stock_moves if move.location_dest_id.usage == 'internal')
            out_qty = sum(move.product_uom_qty for move in stock_moves if move.location_id.usage == 'internal')
            wizard.remaining_qty = in_qty - out_qty

    def action_view_kardex(self):
        self.ensure_one()

        domain = [
            ('product_id', '=', self.product_id.id),
            ('date', '>=', self.date_start),
            ('date', '<=', self.date_end),
            ('state', '=', 'done')
        ]

        stock_moves = self.env['stock.move'].search(domain)
        TempKardexLine = self.env['temp.kardex.line']
        TempKardexLine.search([]).unlink()  # Limpiar registros temporales previos

        remaining_qty = 0
        for move in stock_moves:
            move_type = None  # Inicializa move_type con un valor predeterminado
            if move.location_dest_id.usage == 'internal' and move.location_id.usage != 'internal':
                # Movimiento de entrada
                remaining_qty += move.product_uom_qty
                move_type = 'in'
            elif move.location_id.usage == 'internal' and move.location_dest_id.usage != 'internal':
                # Movimiento de salida
                remaining_qty -= move.product_uom_qty
                move_type = 'out'
            
            # Solo crea el registro si move_type fue asignado
            if move_type:
                TempKardexLine.create({
                    'product_id': move.product_id.id,
                    'date': move.date,
                    'location_id': move.location_id.id,
                    'location_dest_id': move.location_dest_id.id,
                    'product_uom_qty': move.product_uom_qty,
                    'remaining_qty': remaining_qty,
                    'reference': move.reference,
                    'picking_id': move.picking_id.id,
                    'type': move_type,
                })

        return {
            'name': 'Movimientos de Kardex',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'temp.kardex.line',
            'domain': [],
        }
