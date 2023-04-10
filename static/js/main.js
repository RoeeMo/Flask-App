$(document).ready(function() {
  // Show add item modal when Add Item button is clicked
  $("#add-item-btn").click(function() {
    $("#add-item-modal").modal("show");
  });

  // Save new item when Save button is clicked
  $("#save-item-btn").click(function() {
    // Get item details from the form
    var name = $("#item-name").val();
    var price = $("#item-price").val();
    var image = $("#item-image").val();

    // Create new table row with item details
    var newRow = "<tr><td>" + name + "</td><td>$" + price + "</td><td><img src='" + image + "' alt='" + name + "'></td></tr>";

    // Add new row to the table
    $("tbody").append(newRow);

    // Hide the modal
    $("#add-item-modal").modal("hide");

    // Clear the form
    $("#item-name").val("");
    $("#item-price").val("");
    $("#item-image").val("");
  });
});
