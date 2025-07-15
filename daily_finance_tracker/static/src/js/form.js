odoo.define('daily_finance_tracker.form', function(require) {
    "use strict";

    const publicWidget = require('web.public.widget');

    publicWidget.registry.FinanceForm = publicWidget.Widget.extend({
        selector: '#form-wrapper',
        events: {
            'click #add-entry-btn': '_onAddEntry',
            'click #submit-entries-btn': '_onSubmitEntries',
            'click .remove-entry': '_onRemoveEntry',
        },

        start: function() {
            this._super.apply(this, arguments);
            this._onAddEntry(); // add an initial entry row
        },

        _onAddEntry: function() {
            const row = `
                <div class="entry-row border rounded p-3 mb-3">
                    <div class="row">
                        <div class="col-md-3">
                            <select class="form-control flow-type">
                                <option value="inflow">Inflow</option>
                                <option value="outflow">Outflow</option>
                            </select>
                        </div>
                        <div class="col-md-5">
                            <input type="text" class="form-control flow-description" placeholder="Description"/>
                        </div>
                        <div class="col-md-3">
                            <input type="number" class="form-control flow-amount" placeholder="Amount"/>
                        </div>
                        <div class="col-md-1">
                            <button class="btn btn-danger remove-entry" type="button">🗑</button>
                        </div>
                    </div>
                </div> 
            `;
            $('#entries-container').append(row);
        },

        _onRemoveEntry: function (ev) {
            $(ev.currentTarget).closest('.entry-row').remove();
        },

        _onSubmitEntries: function () {
            const date = $('#entry-date').val();
            const entries = [];

            $('.entry-row').each(function () {
                const type = $(this).find('.flow-type').val();
                const description = $(this).find('.flow-description').val();
                const amount = $(this).find('.flow-amount').val();

                if (description && amount) {
                    entries.push({
                        date: date,
                        type: type,
                        description: description,
                        amount: amount
                    });
                }
            });

            if (entries.length === 0) {
                alert("Please fill at least one valid record.");
                return;
            }

            // use ajax call to send entries to the backend
            ajax.jsonRpc("/finance/submit", 'call', {
                entries: entries
            }).then(function () {
                $('#success-msg').removeClass('d-none');
                $('#entries-container').html('');
            });
        },
    });

    return publicWidget.registry.FinanceForm;
});