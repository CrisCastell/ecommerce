(function(){
    const customerInfo = document.querySelector('#customer-info');
    const paypalBox = document.querySelector('#paypal-button-container');
    const proceed = document.querySelector('#proceed');
    let total; 



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
    const csrftokenNew = getToken('csrftoken');

    document.addEventListener('DOMContentLoaded', ()=>{
        paypalBox.style.display = 'none'
    })

    customerInfo.addEventListener('submit', function(e){
        e.preventDefault();
        fetch('/order-info')
        .then(response => response.json())
        .then(data =>{
            total = data.subtotal;
            paypalBox.style.display = 'block';
            disableInp();
            proceed.style.display = 'none'
        })
        .catch(err =>{
            console.log(err)
            //Add error message to the DOM
        })
    })


    function submitData(){
        const data = new FormData(customerInfo);
        
        customData = {
            'address':data.get('address'),
            'city':data.get('city'),
            'state':data.get('state'),
            'zipCode':data.get('zip-code'),
        }
        if (user === 'AnonymousUser'){
            customData.name = data.get('name');
            customData.email = data.get('email');
        }
            
        const url = '/process-order';
        const initObject = {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftokenNew
            },
            body:JSON.stringify({'data':customData})
        }
        fetch(url, initObject)
        .then(response => response.json())
        .then(data => {
            console.log('Success: ', data.message)
            alert(`Transaction Completed: ${data.message}`)
            if(user === 'AnonymousUser'){
                cart = {}
                document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
            }
            location.replace('http://127.0.0.1:8000')
        })
        .catch(err => console.log(err));
    }
    function disableInp(){
        customerInfo.querySelectorAll('input').forEach(inp =>{inp.disabled = true})
    }
    paypal.Buttons({

        // Set up the transaction
        createOrder: function(data, actions) {
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: parseFloat(total).toFixed(2)
                    }
                }]
            });
        },

        // Finalize the transaction
        onApprove: function(data, actions) {
            return actions.order.capture().then(function(details) {
                submitData();
            });
        }


    }).render('#paypal-button-container');
})();