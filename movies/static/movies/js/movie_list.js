window.addEventListener('load', function(){
    const moviePoster = document.querySelectorAll('.movie-poster')
    moviePoster.forEach(function(poster){
        poster.style.height = '500px'
        poster.style.backgroundImage = `url(https://image.tmdb.org/t/p/w342/${poster.dataset.poster})`
        poster.style.backgroundSize = "cover"
    })
})


const likeBtns = document.querySelectorAll('.like-btn')
    likeBtns.forEach(function(btn){
      btn.addEventListener('click', function(event){
        console.log(`${btn.dataset.pk}번 버튼이 눌렸습니다.`)
        axios.get(`/movies/${btn.dataset.pk}/like/`)
        .then(function(res){
            
          if (res.data.liked) {
            btn.style.color = 'crimson'
          } 
          else {
            btn.style.color = 'black'
          }
          const cntSpan = document.querySelector(`.cnt-${btn.dataset.pk}`)
          cntSpan.innerText = res.data.count
        })
        .catch(function(err){
          console.log(err)
        })
      })
})