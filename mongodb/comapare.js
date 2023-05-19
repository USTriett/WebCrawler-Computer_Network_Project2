// Lấy dữ liệu từ file JSON

let perPage = 50;
let idPage = 1;
let start = 0;
let end = perPage;

var product = [];

async function readJSONFile() {
  const response = await fetch('json/newProducts.json');
  const data = await response.json();
  data.forEach(function (items){
    var temp = [];
    temp = items.Products;
    temp.forEach(function (item){
        if(item.Imgs[0] === null)
            item.Imgs[0] = 'img/TvT.png';
    });
  });
  product = data;
  console.log(product); // In mảng ra console
  console.log(product[0].Desc[0]);
  console.log(product[0].Desc[0].CPU);
}

async function main() {
    await readJSONFile();
let productArr = [];
productArr = product;

const pageConfig = document.querySelector('.page-config select');
const mySelect = document.getElementById('mySelect');
const countTotalPage = document.querySelector('.total-page');
const countTotalProduct = document.querySelector('.total-item');

let totalPages = Math.ceil(productArr.length / perPage);
const searchText = document.querySelector('.searchText');
const searchBtn = document.getElementById('search');

function highlightText() {
    const title = document.querySelectorAll('.content__product__item h3');
    title.forEach((title, index) => {
        let titleText = title.innerHTML;
        let indexOf = Number(titleText.toLocaleLowerCase().indexOf(searchText.value.toLocaleLowerCase()));
        let searchTextLength = searchText.value.length;
        titleText = titleText.substring(0, indexOf) + "<span class='highlight'>" + titleText.substring(indexOf, indexOf + searchTextLength) + "</span>" + titleText.substring(indexOf + searchTextLength, titleText.length);
        title.innerHTML = titleText;
        console.log(titleText);
    })
}

function initRender(productAr, totalPage) {
    renderProduct(productAr);
    renderListPage(totalPage);
}

function getCurrentPage(indexPage) {
    start = (indexPage - 1) * perPage;
    end = indexPage * perPage;
    totalPages = Math.ceil(productArr.length / perPage);
    countTotalPage.innerHTML = `Total pages: ${totalPages}`;
    countTotalProduct.innerHTML = `Total Product:  ${productArr.length}`
}


function renderListPage(totalPages) {
    let html = '';
    html += `<li class="current-page active"><a>${1}</a></li>`;
    for (let i = 2; i <= 10; i++) {
        html += `<li><a>${i}</a></li>`;
    }
    if (totalPages === 0) {
        html = ''
    }
    document.getElementById('number-page').innerHTML = html;
}

function changePage() {
    const idPages = document.querySelectorAll('.number-page li');
    const a = document.querySelectorAll('.number-page li a');
    for (let i = 0; i < idPages.length; i++) {
        idPages[i].onclick = function () {
            let value = i + 1;
            const current = document.getElementsByClassName('active');
            current[0].className = current[0].className.replace('active', '');
            this.classList.add('active');
            if (value > 1 && value < idPages.length) {
                $('.btn-prev').removeClass('btn-active');
                $('.btn-next').removeClass('btn-active');
            }
            if (value == 1) {
                $('.btn-prev').addClass('btn-active');
                $('.btn-next').removeClass('btn-active');
            }
            if (value == idPages.length) {
                $('.btn-next').addClass('btn-active');
                $('.btn-prev').removeClass('btn-active');
            }
            idPage = value;
            getCurrentPage(idPage);
            renderProduct(productArr);
        };
    }
}

initRender(productArr, totalPages);
getCurrentPage(1);

searchBtn.addEventListener('click', () => {
    idPage = 1;
    productArr = [];
    product.forEach((item, index) => {
        if (item.NameCategory.toLocaleLowerCase().indexOf(searchText.value.toLocaleLowerCase()) != -1) {
            productArr.push(item);
            productArr.sort(function(pd1, pd2){
                return pd1["CatePrice"] - pd2["CatePrice"];
            })
        }
    });
    if (productArr.length === 0) {
        $('.no-result').css('display', 'block')
    } else {
        $('.no-result').css('display', 'none')
    }
    getCurrentPage(idPage);
    initRender(productArr, totalPages);
    changePage();
    if (totalPages <= 1) {
        $('.btn-prev').addClass('btn-active');
        $('.btn-next').addClass('btn-active');
    } else {
        $('.btn-next').removeClass('btn-active');
    }
});

searchText.addEventListener("keyup", (event) => {
    if (event.keyCode === 13) {
        event.preventDefault();
        searchBtn.click();
    }
});

pageConfig.addEventListener('change', () => {
    idPage = 1;
    perPage = Number(pageConfig.value);
    getCurrentPage(idPage);
    initRender(productArr, totalPages);
    if (totalPages == 1) {
        $('.btn-prev').addClass('btn-active');
        $('.btn-next').addClass('btn-active');
    } else {
        $('.btn-next').removeClass('btn-active');
    }
    changePage();
});

function renderProduct(product) {
    html = '';
    $.each(product, function (i, products) {
        console.log(typeof JSON.stringify(products.Desc));
        html += `
        <div class = "product__item">
            <form action="result.html" method="GET">
                <label for="name_cate" style = "display: none">Name Category:</label>
                <input type="text" id="name_cate" name="name_cate" style = "display: none" value = "${products.NameCategory}" readonly>
                
                <label for="cate_price" style = "display: none">CatePrice:</label>
                <input type="number" id="cate_price" name="cate_price" style = "display: none" value = ${products.CatePrice} readonly>

                <label for="desc" style = "display: none">CatePrice:</label>
                <input type="text" id="desc" name="desc" style = "display: none" value = ${JSON.stringify(products.Desc)} readonly>
                `
        html += `
        <!--
                <div style = "border-style: groove; max-width: 800px">
                    <p>${products.NameCategory}</p>
                    <p> ${products.CatePrice} đồng</p>
                    <p> ${JSON.stringify(products.Desc)} </p>
                    <button type="submit">Đến trang so sánh</button>
                </div>
        -->

            <div class="container-fluid bg-trasparent my-4 p-3" style= "max-width: 400px;">
                <div class="card h-100 shadow-sm">
                <a href="#">
                    <img src=${products.CateImgs[0]} class="card-img-top" alt="product.title" />
 
                </a>
        
                <div class="card-body">

                    

                    <h5 class="card-title">
                        <p target="_blank"><strong>${products.NameCategory}</strong></p>

                    </h5>
                    <div class = "container estimate">
                        <span class="float-start badge rounded-pill" > </span>
        
                        <span class="float-end"><a href="#" class="small text-muted text-uppercase aff-link rounded-pill" >${products.CatePrice} VNĐ</a></span>
                    </div>
                    <!--
                    <div class="container test" style = "justify-content: center">
                         <img src="https://upload.wikimedia.org/wikipedia/commons/6/64/Logo_Tiki.png" class="card-brand" alt="product.title"/>  
                        <p><strong>${products.CatePrice} đồng<strong></p>
                    </div>
                    -->

                    </div>
                    <div class="productCardPrice">
                        <button type = "submit" class="btn btn-warning bold-btn">Đến trang so sánh</a>
        
                    </div>

                    <div class = "container estimate">
        
                        <span class="float-start">
                            <div class="d-flex flex-row user-ratings">
                                <div class="ratings">
                                    <i class="fa fa-star"></i>
                                    <i class="fa fa-star"></i>
                                    <i class="fa fa-star"></i>
                                    <i class="fa fa-star"></i>
                                </div>
                                <h6 class="text-muted ml-1">4/5</h6>
                            </div>
                        </span>
        
                        <span class="heartsymbol">
                            <i class="far fa-heart" style="cursor: pointer"></i>
        
                        </span>
                    </div>
                </div>
            </div>

                `
        html += `
                <label for="img_len" style = "display: none">ImgLen:</label>
                <input type="number" id = "img_len" style = "display: none" name = "img_len" value = ${products.CateImgs.length} readonly>
                <label for="number_of_products" style = "display: none">Number of products:</label>
                <input type="number" id="num_prods" name="num_prods" style = "display: none" value = ${products.Products.length} readonly>
                `

        for (var i = 0; i < products.CateImgs.length; i++) {

            html += `
                <label for="img_link_1" style = "display: none">ImgLink${i}:</label>
                <input type="text" id = "img_link" name = "img_link_${i}" style = "display: none" value = "${products.CateImgs[i]}" readonly>
                `
        }

        for (var i = 0; i < products.Products.length; i++) {
            html += `
                <label for="product_${i}_name" style = "display: none">Product ${i} Name:</label>
                <input type="text" id = "product_${i}_name" style = "display: none" name = "product_${i}_name" value = "${products.Products[i]['Name']}" readonly>
                
                <label for="product_${i}_name" style = "display: none">Product ${i} Url:</label>
                <input type="text" id = "product_${i}_url" style = "display: none" name = "product_${i}_url" value = "${products.Products[i]['Url']}" readonly>
                
                <label for="product_${i}_price" style = "display: none">Product ${i} price:</label>
                <input type="number" id = "product_${i}_price" name = "product_${i}_price" style = "display: none" value = ${products.Products[i]['Price']} readonly>
                
                <label for="product_${i}_original_price" style = "display: none">Product ${i} price before sale:</label>
                <input type="number" id = "product_${i}_original_price" style = "display: none" name = "product_${i}_original_price" value = ${products.Products[i]['OriginalPrice']} readonly>
                
                <label for="product_${i}_img" style = "display: none">Product ${i} img:</label>
                <input type="text" id = "product_${i}_img" name = "product_${i}_img" style = "display: none" value = "${products.Products[i]["Imgs"]}" readonly>
                
                <label for="product_${i}_web_icon" style = "display: none">Product ${i} web icon:</label>
                <input type="text" id = "product_${i}_web_icon" name = "product_${i}_web_icon" style = "display: none" value = "${products.Products[i]['WebIcon']}" readonly>
                
                `
        }
        html +=
            `
            </form>
        </div>
        
        `
    })
    document.getElementById('product').innerHTML = html;
    highlightText();
}

changePage();

$('.btn-next').on('click', () => {
    idPage++;
    if (idPage > totalPages) {
        idPage = totalPages;
    }
    if (idPage == totalPages) {
        $('.btn-next').addClass('btn-active');
    } else {
        $('.btn-next').removeClass('btn-active');
    }
    console.log(idPage);
    const btnPrev = document.querySelector('.btn-prev');
    btnPrev.classList.remove('btn-active');
    $('.number-page li').removeClass('active');
    $(`.number-page li:eq(${idPage - 1})`).addClass('active');
    getCurrentPage(idPage);
    renderProduct(productArr);
});

$('.btn-prev').on('click', () => {
    idPage--;
    if (idPage <= 0) {
        idPage = 1;
    }
    if (idPage == 1) {
        $('.btn-prev').addClass('btn-active');
    } else {
        $('.btn-prev').removeClass('btn-active');
    }
    const btnNext = document.querySelector('.btn-next');
    btnNext.classList.remove('btn-active');
    $('.number-page li').removeClass('active');
    $(`.number-page li:eq(${idPage - 1})`).addClass('active');
    getCurrentPage(idPage);
    renderProduct(productArr);
});
}

main();

// const fs = require('fs');

// const url = 'https://web-crawler-computer-network-project2.vercel.app/getData';

// function writeData(data){
    
//     var x=JSON.stringify(data, null, 2);
//     fs.writeFile('json/newProducts.json', x, (error) => {
//         if (error) throw error;
//         console.log('Data written to file');
//     });
// }


// fetch(url, {
//     method: 'POST',
//     headers: {
//         'Content-Type': 'application/json'
//     }
// })
// .then(response => response.json())
// .then(data => writeData(data))
// .catch(error => console.error(error));


