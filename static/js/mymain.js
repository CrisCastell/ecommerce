(function(window){
    const categoryBtn = document.querySelector('#category');
    const catBox = document.querySelector('#cat-box');
    const header =  document.querySelector('header');
    const nav = document.querySelector('nav')
    const searchBar = document.querySelector('#search-bar');
    const navBtn = document.querySelectorAll('.nav-btn');
    const overlay = document.querySelector('#overlay');
    const miniTotal = document.querySelectorAll('.mini-total');
    const profileBox = document.querySelector('#profile-box');
    let profileBtn;



    /* First, get or generate cookie */
    function getCookie(name){
        const cookieArr = document.cookie.split(";");

        for(let i = 0; i < cookieArr.length; i++){
            const cookiePair = cookieArr[i].split("=");
            if(name == cookiePair[0].trim()){
                return decodeURIComponent(cookiePair[1]);
            }
        }
        

        return null;
    }

    let cart = JSON.parse(getCookie('cart'));


    if (cart == undefined){
        console.log('Cart es null')
        cart = {}
        console.log('Cart was created!')
        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
        
    }


    /* get CSRF token */
    function getToken(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }





    /* Header, Dropdowns & Nav */

    categoryBtn.addEventListener('click', ()=>{
        catBox.style.top = `${header.getBoundingClientRect().bottom}px`;
        catBox.style.right = `${document.querySelector('body').clientWidth - categoryBtn.getBoundingClientRect().right}px`;
        catBox.style.display = 'flex'
        
        catBox.classList.toggle('active');
    })


    document.addEventListener('DOMContentLoaded', function(){
        if(document.querySelector('#mini-profile') != null){
            profileBtn = document.querySelector('#mini-profile');
            profileBtn.addEventListener('click', function(){
                let profileBtnPosition = profileBtn.getBoundingClientRect();
                profileBox.style.right = `${document.querySelector('body').clientWidth - profileBtnPosition.right}px`;
                profileBox.style.display = 'flex'
                profileBox.style.top = `${header.getBoundingClientRect().bottom}px`
                // profileBox.style.width = `${profileBtnPosition.width}px`;
                profileBox.classList.toggle('active');
            })
        }
        // loadIcons();
    })

    document.addEventListener('click', function(e){
        
        if(profileBtn != null){
            if(e.target.id === 'mini-profile' || e.target.class === 'li-btn' /*|| e.target.id ==='mini-pic' || e.target.id ==='user-name'*/){
                return
            }
            else{
                profileBox.classList.remove('active');
            }
        }
        if(catBox.style.display != 'none'){
            if(e.target.class === 'li' || e.target.id === 'cat-ul' || e.target.id === 'cat-box' || e.target.id === 'category'){
                return
            }
            else{
                catBox.classList.remove('active');
            }
        }
    })


    navBtn.forEach( function(button){
        button.addEventListener('click', function(){
            nav.classList.toggle('active');
            overlay.classList.toggle('active');
        })
    })



    overlay.addEventListener('click', function(){
        nav.classList.remove('active');

        overlay.classList.remove('active');
    })

    // window.addEventListener('resize', ()=>{
    //     loadIcons();
    // })

    // function loadIcons(){
    //     if(window.innerWidth <=  1060){
    //         nav.querySelectorAll('a').forEach(a =>{
    //             if(a.dataset.icon != undefined){
    //                 a.classList.add(`flaticon-${a.dataset.icon}`)
    //             }
                
    //         })
    //     }
    // }
    /* Update quantities and order items */
    const updateButtons = document.querySelectorAll('.update-order');
    const totalItems = document.querySelectorAll('.total-items');
    const subtotals = document.querySelectorAll('.subtotal');
    const csrftoken = getToken('csrftoken');
    const detailBtn = document.querySelector('#detail-button');









    /* Handle order updates */
    document.addEventListener('DOMContentLoaded', ()=>{
        
        loadInfo();
        if(detailBtn != null){
            detailBtn.addEventListener('click', function(){
                
                if(user === 'AnonymousUser'){
                    addCookieItem(this.dataset);
                }
                else{
                    updateOrder(this.dataset);
                }
                setTimeout(function(){
                    window.location.replace('/cart')
                }, 500)
            })        
        }
        
    })

    updateButtons.forEach(button =>{
        button.addEventListener('click', function(){
            if(user == 'AnonymousUser'){
                addCookieItem(this.dataset);
            }
            else{
                updateOrder(this.dataset);
                console.log('va bien en el trigger')
            }
            
        })
    })









    const loadInfo = async() =>{
        try {
            const res = await fetch('/order-info');
            let data = await res.json();

            miniTotal.forEach(elem => elem.innerHTML = data.totalItems);
            
            if(totalItems != null && subtotals != null){
                totalItems.forEach(totalItem =>{
                    totalItem.innerHTML = data.totalItems;
                })
                
                subtotals.forEach(elem => {
                    elem.innerHTML= data.subtotal;
                    subtotal = data.subtotal;
                })
            }
            
            

        } catch(err) {
            console.error(err);
        }
    }



    function addCookieItem(dataset){

        if(dataset.action == 'add'){
            if (cart[dataset.product] === undefined){
                cart[dataset.product] = {'quantity':1}
            }
            else{
                cart[dataset.product]['quantity'] += 1;
            }
        }
        if(dataset.action == 'remove'){
            cart[dataset.product]['quantity'] -= 1;
            if(cart[dataset.product]['quantity'] <= 0){
                console.log('Remove item')
                
                delete cart[dataset.product]
                document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
                window.location.reload()
                return
            }
        }
        
        let id = document.getElementById(`quantity-${dataset.product}`);
        if(id != null){
            id.innerHTML = cart[dataset.product]['quantity'];
        }
        
        console.log('Cart: ', cart);
        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
        loadInfo();
    }


    function updateOrder(dataset){
        const url = `/update-order`;
        
        const initObject = {
            method:'POST',
            headers:{
                'Content':'application/json',
                'X-CSRFToken': csrftoken
            },
            body:JSON.stringify({
                'productId':dataset.product,
                'action':dataset.action
            })
        }
        
        fetch(url, initObject)
        .then(response => response.json())
        .then(data => {
            updateQuantity(data);
            loadInfo();

        })
        .catch(err => console.log(err))
    }


    function updateQuantity(data){
        const id=document.getElementById(`quantity-${data.id}`);
        console.log(data);
        if( id != null){
            if(data.deleted == true){
                window.location.reload()
            }
            else{
                id.innerHTML = data.quantity;
            }
        }
    }
})(window);

