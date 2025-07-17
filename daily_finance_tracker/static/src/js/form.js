odoo.define('daily_finance_tracker.form', [], function(require) {
    'use strict';

    // Use DOM ready approach for frontend JavaScript
    $(document).ready(function() {
        
        // Initialize the form
        addEntry(); // Load one row by default
        
        // Add entry button handler
        $('#add-entry-btn').on('click', function() {
            addEntry();
        });
        
        // Remove entry button handler (using event delegation)
        $(document).on('click', '.remove-entry', function() {
            $(this).closest('.entry-row').remove();
        });
        
        // Submit entries button handler
        $('#submit-entries-btn').on('click', function() {
            submitEntries();
        });
        
        function addEntry() {
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
        }
        
        function submitEntries() {
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

            // Use jQuery AJAX with proper JSON-RPC format
            $.ajax({
                url: '/finance/submit',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    jsonrpc: '2.0',
                    method: 'call',
                    params: { entries: entries },
                    id: Math.floor(Math.random() * 1000)
                }),
                success: function(response) {
                    if (response.result && response.result.status === 'success') {
                        $('#success-msg').removeClass('d-none');
                        $('#entries-container').html('');
                        addEntry(); // Add one empty row back
                    } else {
                        alert('Error submitting entries. Please try again.');
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Error submitting entries:', error);
                    alert('Error submitting entries. Please try again.');
                }
            });
        }
    });
});