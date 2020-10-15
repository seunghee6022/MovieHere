let chooseCnt1 = 0
let chooseCnt2 = 0
let chooseCnt3 = 0

const withWhomBtns = document.querySelectorAll('.withWhom')
// const feelingBtns = document.querySelectorAll('.feeling')
// const lifeBtns = document.querySelectorAll('.life')

withWhomBtns.forEach(function(btn){

    btn.addEventListener('click', function(e){
        console.log(btn)
        e.preventDefault()
        const btnClasses1 = btn.classList

        if (btn.className.includes('btn-secondary')) {
            if (chooseCnt1 == 1) {
                alert('1개만 골라주세요.')
            } else {
                btnClasses1.remove('btn-secondary')
                btnClasses1.add('btn-danger')
                chooseCnt1 += 1
            }
        } else {
            btnClasses1.remove('btn-danger')
            btnClasses1.add('btn-secondary')
            chooseCnt1 -= 1
        }
    })
})
// feelingBtns.forEach(function(btn){

//     btn.addEventListener('click', function(e){
//         e.preventDefault()
//         const btnClasses2 = btn.classList

//         if (btn.className.includes('btn-secondary')) {
//             if (chooseCnt2 == 1) {
//                 alert('1개만 골라주세요.')
//             } else {
//                 btnClasses2.remove('btn-secondary')
//                 btnClasses2.add('btn-warning')
//                 chooseCnt2 += 1
//             }
//         } else {
//             btnClasses2.remove('btn-warning')
//             btnClasses2.add('btn-secondary')
//             chooseCnt2 -= 1
//         }
//     })
// })

// lifeBtns.forEach(function(btn){

//     btn.addEventListener('click', function(e){
//         e.preventDefault()
//         const btnClasses3 = btn.classList

//         if (btn.className.includes('btn-secondary')) {
//             if (chooseCnt3 == 3) {
//                 alert('3개 까지만 고를 수 있습니다.')
//             } else {
//                 btnClasses3.remove('btn-secondary')
//                 btnClasses3.add('btn-success')
//                 chooseCnt3 += 1
//             }
//         } else {
//             btnClasses3.remove('btn-success')
//             btnClasses3.add('btn-secondary')
//             chooseCnt -= 1
//         }
//     })
// })


const goRecommend = document.querySelector('#goRecommend')
goRecommend.addEventListener('click', function(e){
    e.preventDefault()

    if (chooseCnt1 != 1 or chooseCnt2 != 1 or chooseCnt3 != 1 ) {
        alert('혹시 선택안한 질문이 있나요?')

    } else {
        // let chooseList = []
        const chooseWhom = document.querySelectorAll(".btn-danger")
        // const chooseFeeling = document.querySelectorAll(".btn-warning")
        // const chooseLife = document.querySelectorAll(".btn-success")
        // chooseList.forEach(function(g){
        //     recList.push(g.textContent)
        // })
        chooseList.push(chooseWhom.textContent)
        // chooseList.push(chooseFeeling.textContent)
        // chooseList.push(chooseLife.textContent)


        // chooseList = chooseList.join(",")
        axios.get(`/movies/movieherechoice/`, {
            params: {
                'chooseWhom': chooseWhom,
                // 'chooseFeeling' : chooseFeeling,
                // 'chooseLife':chooseLife,

            }
        })
        .then(function(res){
            console.log(res.data)
        })
    }
})