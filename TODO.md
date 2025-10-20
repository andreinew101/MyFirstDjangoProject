# TODO: Add "Update Stocks" Feature

## Steps to Complete

- [x] Add `update_stock` view in `fdjangoproj/systemuser/views.py` to handle adding/deducting quantity for an item, with validation to prevent negative quantity.
- [x] Add URL pattern for `update_stock` in `fdjangoproj/systemuser/urls.py`.
- [x] Modify `fdjangoproj/templates/systemuser/item_list.html` to include an "Update Stock" button for each item.
- [x] Create new template `fdjangoproj/templates/systemuser/update_stock.html` for the update form (add/deduct amount).
- [x] Add "Update Stocks" link to the sidebar in `fdjangoproj/templates/partials/sidebar.html`, pointing to the item_list view.
- [ ] Test the feature by logging in as Admin, Manager, and Employee to ensure access and functionality.
- [ ] Verify success/error messages are displayed correctly.
