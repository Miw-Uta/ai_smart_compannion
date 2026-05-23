// alert('表格的增删改查')
// 新增数据函数
function addrow() {
 let table = document.getElementById('table');
//  console.log(table);
// 获取表格插入的位置
 let length = table.rows.length;
//  console.log (length)

// 插入行节点
let newrow = table.insertRow(length);
console.log (newrow)
// newrow.innerHTML=('123456')

// 插入列节点对象
let nameCol = newrow.insertCell(0);
let phoneCol = newrow.insertCell(1);
let actionCol = newrow.insertCell(2);
// 修改节点文本对象
nameCol.innerHTML=('未命名')
phoneCol.innerHTML=('无联系方式')
actionCol.innerHTML=('<button onclick=" editrow(this)">编辑</button> <button onclick="delrow(this)">删除</button>')
}


// 删除数据函数
function delrow (button) {
    console.log(button)
    let row = button.parentNode.parentNode;
    console.log (row)
    row.parentNode.removeChild(row)
}


// 编辑数据函数
function editrow(button) {
    console.log (button)
    let row = button.parentNode.parentNode;
    console.log(row);
    let name = row.cells[0]
    let phone = row.cells[1]
    
    let inputname = prompt('请输入姓名')
    let inputphone = prompt('请输入联系方式')

    // name.innerHTML=inputname
    // phone.innerHTML=inputphone




    
    // 改进内容

    let oringnalName = name.innerText;
    let oringnalPhone = phone.innerText;
   
    if (!inputname && !inputphone) {
        alert('编辑内容为空，编辑失败')
    }else if (!inputname){
        name.innerHTML=oringnalName
        phone.innerHTML=inputphone
    }else if (!inputphone){
        name.innerHTML=inputname
        phone.innerHTML=oringnalPhone
    }else{
    name.innerHTML=inputname
    phone.innerHTML=inputphone
    }
}