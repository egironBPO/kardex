from odoo import models, fields

class TempKardexLine(models.TransientModel):  # Si es un modelo transitorio (temporal)
    _name = 'temp.kardex.line'
    _description = 'Línea Temporal de Kardex'

    product_id = fields.Many2one('product.product', string='Producto')
    date = fields.Datetime(string='Fecha')
    location_id = fields.Many2one('stock.location', string='Origen')
    location_dest_id = fields.Many2one('stock.location', string='Destino')
    product_uom_qty = fields.Float(string='Cantidad')
    remaining_qty = fields.Float(string='Cantidad Restante')
    reference = fields.Char(string='Referencia')
    picking_id = fields.Many2one('stock.picking', string='Picking')
    type = fields.Selection([('in', 'Entrada'), ('out', 'Salida')], string='Tipo')