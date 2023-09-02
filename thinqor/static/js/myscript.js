function updateCartItemCount() {
    $.ajax({
        url: 'get_cart_item_count', // Replace with your Django URL
        type: 'GET',
        success: function(data) {
            // Update the cart item count in the badge
            $('.badge-pill').text(data.cart_item_count);
        },
        error: function(error) {
            console.error('Error updating cart item count: ' + error);
        }
    });
}
$(document).ready(function() {
    // Update the cart item count immediately when the page loads
    updateCartItemCount();

    // Add an event listener to update the count when the button is clicked
    $('#add-to-cart-button').click(function() {
        // Perform the logic to add the item to the cart
        // ...

        // Update the cart item count
        updateCartItemCount();
    });
});




