function openSearchPage() {
    window.location.href = '/search';
}

function logout() {
    window.location.href = '/logout'; 
}

setTimeout(function() {
    var flashMessage = document.getElementById('flash-message');
    if (flashMessage) {
        flashMessage.style.display = 'none';
    }
}, 2000);









//favorite-btn home
var addTofavourite = document.querySelectorAll('.favourite-btn');
addTofavourite.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var itemName = button.getAttribute('data-item-name');
        var description = button.getAttribute('data-description');
        var price = button.getAttribute('data-price');
        addfavHome(itemName, description, price);
    });
});
function addfavHome(itemName, description, price) {
    window.location.href = '/handle-Add-to-favourite-from-home?ItemName=' + encodeURIComponent(itemName) + '&Description=' + encodeURIComponent(description) + '&Price=' +encodeURIComponent(price);
}

// for unblock-resturant
var unblockresturant = document.querySelectorAll('.unblock-resturant');
unblockresturant.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var id = button.getAttribute('id');
        unblockresturantt(id);
    });
});
function unblockresturantt(id) {
    window.location.href = '/handle-unblock-resturant?id=' + encodeURIComponent(id);
}



// for unblock-user
var unblockuser = document.querySelectorAll('.unblock-user');
unblockuser.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var id = button.getAttribute('id');
        unblockuser(id);
    });
});
function unblockuser(id) {
    window.location.href = '/handle-unblock-user?id=' + encodeURIComponent(id);
}


//for block-resturant
var blockresturant = document.querySelectorAll('.block-resturant');
blockresturant.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var id = button.getAttribute('id');
        blockresturantt(id);
    });
});
function blockresturantt(id) {
    window.location.href = '/handle-block-resturant?id=' + encodeURIComponent(id);
}

//for block-user
var blockuser = document.querySelectorAll('.block-user');
blockuser.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var id = button.getAttribute('id');
        blockuser(id);
    });
});
function blockuser(id) {
    window.location.href = '/handle-block-user?id=' + encodeURIComponent(id);
}



// for remove Admin
var removeAdmin = document.querySelectorAll('.remove-admin');
removeAdmin.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var Name = button.getAttribute('data-name');
        var email = button.getAttribute('data-email');
        removeAdmin(Name,email);
    });
});
function removeAdmin(name, email) {
    window.location.href = '/handle-remove-admin?name=' + encodeURIComponent(name) + '&email=' + encodeURIComponent(email);
}






// for add to cart on search page
var addToCartButtonSearch = document.querySelectorAll('.add-to-cart-btn-search');
addToCartButtonSearch.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var itemName = button.getAttribute('data-item-name');
        var description = button.getAttribute('data-description');
        var price = button.getAttribute('data-price');
        addToCartSearch(itemName, description, price);
    });
});
function addToCartSearch(itemName, description, price) {
    window.location.href = '/handle-Add-to-cart-from-search?ItemName=' + encodeURIComponent(itemName) + '&Description=' + encodeURIComponent(description) + '&Price=' +encodeURIComponent(price);
}










// for add to cart on home for promotions
var addToCartButtonsPromotion = document.querySelectorAll('.add-to-cart-btn-promortion');
addToCartButtonsPromotion.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var PromotionName = button.getAttribute('data-PromotionName');
        var discount = button.getAttribute('data-discount');
        addToCartPromotionHome(PromotionName, discount);
    });
});
function addToCartPromotionHome(PromotionName, discount) {
    window.location.href = '/handle-Add-to-cart-Promotion-from-home?PromotionName=' + encodeURIComponent(PromotionName) + '&discount=' + encodeURIComponent(discount);
}





// For add to cart in home for menu items
var addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
addToCartButtons.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var itemName = button.getAttribute('data-item-name');
        var description = button.getAttribute('data-description');
        var price = button.getAttribute('data-price');
        addToCart(itemName, description, price);
    });
});
function addToCart(itemName, description, price) {
    window.location.href = '/handle-Add-to-cart-from-home?ItemName=' + encodeURIComponent(itemName) + '&Description=' + encodeURIComponent(description) + '&Price=' +encodeURIComponent(price);
}