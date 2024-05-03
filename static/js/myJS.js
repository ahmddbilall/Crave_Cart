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
}, 4000);









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

// for add to cart on search page
var addToCartButtonrecommend = document.querySelectorAll('.add-to-cart-btn-recommend');
addToCartButtonrecommend.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var itemName = button.getAttribute('data-item-name');
        var description = button.getAttribute('data-description');
        var price = button.getAttribute('data-price');
        addToCartrecommend(itemName, description, price);
    });
});
function addToCartrecommend(itemName, description, price) {
    window.location.href = '/handle-Add-to-cart-from-recommend?ItemName=' + encodeURIComponent(itemName) + '&Description=' + encodeURIComponent(description) + '&Price=' +encodeURIComponent(price);
}




// for add to cart on search page
var addToCartButtonfavourite = document.querySelectorAll('.add-to-cart-btn-favourites');
addToCartButtonfavourite.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var itemName = button.getAttribute('data-item-name');
        var description = button.getAttribute('data-description');
        var price = button.getAttribute('data-price');
        addToCartfavourite(itemName, description, price);
    });
});
function addToCartfavourite(itemName, description, price) {
    window.location.href = '/handle-Add-to-cart-from-favourite?ItemName=' + encodeURIComponent(itemName) + '&Description=' + encodeURIComponent(description) + '&Price=' +encodeURIComponent(price);
}


// for add to cart on discount 
var addToCartButtonsPromotionDiscounts = document.querySelectorAll('.add-to-cart-btn-discount');
addToCartButtonsPromotionDiscounts.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var PromotionName = button.getAttribute('data-name');
        addToCartPromotionDiscount(PromotionName);
    });
});
function addToCartPromotionDiscount(PromotionName) {
    window.location.href = '/handle-Add-to-cart-from-discount?PromotionName=' + encodeURIComponent(PromotionName);
}







// remove from cart
var cartItemDelete = document.querySelectorAll('.text-danger');
cartItemDelete.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var menuid = button.getAttribute('data-menuid');
        removeFromCart(menuid)

    });
});
function removeFromCart(menuid) {
    window.location.href = '/handle-remove-from-cart?menuid=' + encodeURIComponent(menuid);
}



//add or edit instruction
var saveButtonInstructionCart = document.querySelectorAll('.save-button');
saveButtonInstructionCart.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var form = button.closest('.form');
        var instruction = form.querySelector('.form__field').value;
        var menuid = button.getAttribute('data-menuid');
        var quantity = document.getElementById('quantityInput').value;

        instructionCart(menuid, instruction,quantity);
    });
});
function instructionCart(menuid,instruction,quantity) {
    window.location.href = '/handle-instruction-from-cart?menuid=' + encodeURIComponent(menuid)+ '&instruction=' + encodeURIComponent(instruction)+ '&quantity=' + encodeURIComponent(quantity);
}

//orderButtonCart
var orderButtonInstructionCart = document.querySelectorAll('.orderButtonCart');
orderButtonInstructionCart.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        placeorder();
    });
});
function placeorder() {
    var selectElement = document.getElementById('order-type');
    var selectedValue = selectElement.value;
    window.location.href = '/handle-order-from-cart?type=' + encodeURIComponent(selectedValue);
}


// for add to cart on home for promotions
document.addEventListener('click', function(event) {
    if (event.target.matches('.add-to-cart-btn-promortion')) {
        event.preventDefault();
        var button = event.target;
        var PromotionName = button.getAttribute('data-PromotionName');
        var discount = button.getAttribute('data-discount');
        addToCartPromotionHome(PromotionName, discount);
    }
});
function addToCartPromotionHome(PromotionName, discount) {
    window.location.href = '/handle-Add-to-cart-Promotion-from-home?PromotionName=' + encodeURIComponent(PromotionName) + '&discount=' + encodeURIComponent(discount);
}





//add to favourites from discount
var addtofavouriteDiscount = document.querySelectorAll('.favorite-btn-discount');
addtofavouriteDiscount.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var PromotionName = button.getAttribute('data-name');
        addToFavPromotionHome(PromotionName);
    });
});
function addToFavPromotionHome(PromotionName) {
    window.location.href = '/handle-Add-to-fav-Promotion-from-discount?PromotionName=' + encodeURIComponent(PromotionName);
}



//remove from favourites from favourite
var removetofavouriteDiscount = document.querySelectorAll('.favorite-btn-favourite');
removetofavouriteDiscount.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var itemName = button.getAttribute('data-item-name');
        var description = button.getAttribute('data-description');
        var price = button.getAttribute('data-price');
        removeToFavHome(itemName, description, price);
    });
});
function removeToFavHome(itemName, description, price) {
    window.location.href = '/handle-remove-to-favourite-from-favourites?ItemName=' + encodeURIComponent(itemName) + '&Description=' + encodeURIComponent(description) + '&Price=' +encodeURIComponent(price);
}



//add to favourites from home
var addtofavouriteHome = document.querySelectorAll('.favorite-btn');
addtofavouriteHome.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var itemName = button.getAttribute('data-item-name');
        var description = button.getAttribute('data-description');
        var price = button.getAttribute('data-price');
        addToFavHome(itemName, description, price);
    });
});
function addToFavHome(itemName, description, price) {
    window.location.href = '/handle-Add-to-favourite-from-home?ItemName=' + encodeURIComponent(itemName) + '&Description=' + encodeURIComponent(description) + '&Price=' +encodeURIComponent(price);
}


//add to favourites from search
var addtofavouritesearch = document.querySelectorAll('.favorite-btn-search');
addtofavouritesearch.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var itemName = button.getAttribute('data-item-name');
        var description = button.getAttribute('data-description');
        var price = button.getAttribute('data-price');
        addToFavSearch(itemName, description, price);
    });
});
function addToFavSearch(itemName, description, price) {
    window.location.href = '/handle-Add-to-favourite-from-search?ItemName=' + encodeURIComponent(itemName) + '&Description=' + encodeURIComponent(description) + '&Price=' +encodeURIComponent(price);
}



//add to favourites from recommend
var addtofavouriterecommend = document.querySelectorAll('.favorite-btn-recommend');
addtofavouriterecommend.forEach(function(button) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        var itemName = button.getAttribute('data-item-name');
        var description = button.getAttribute('data-description');
        var price = button.getAttribute('data-price');
        addToFavrecommend(itemName, description, price);
    });
});
function addToFavrecommend(itemName, description, price) {
    window.location.href = '/handle-Add-to-favourite-from-recommend?ItemName=' + encodeURIComponent(itemName) + '&Description=' + encodeURIComponent(description) + '&Price=' +encodeURIComponent(price);
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