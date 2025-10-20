# TODO: Add Update Stock Feature

- [x] Create UpdateStockForm in forms.py with quantity_change field (IntegerField, allows negative values).
- [x] Create update_stock view in views.py: GET shows form with current quantity displayed, POST validates change, updates quantity (ensuring >=0), saves, redirects to item_list.
- [x] Add URL pattern in urls.py for update_stock/<int:pk>/.
- [x] Create update_stock.html template: form with current quantity display, input for quantity change, submit button.
- [x] Modify item_list.html: add "Update Stock" button in Actions column, linking to update_stock URL.
- [ ] Test the feature: run server, update stock, ensure no negative quantities, messages shown.
