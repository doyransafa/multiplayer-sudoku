let pathNameArray = window.location.pathname.split("/")
let roomName = pathNameArray[pathNameArray.length - 1]
let socketUrl = `ws://${window.location.host}/ws/room/${roomName}`
const updatesContainer = document.getElementById('messages')
const currentUser = document.getElementById('current-user')
const buttons = document.querySelectorAll(".button")
const finishedBanner = document.getElementById("finished-banner")
const chatSocket = new WebSocket(socketUrl)
const scoreboard = document.getElementById("scoreboard")

let form = document.getElementById("form")
form.addEventListener("submit", (e) => {
	e.preventDefault()
	let message = e.target.message.value
	if (message != '') {
		chatSocket.send(
			JSON.stringify({
				type: "chat_message",
				username: currentUser.innerHTML,
				message: message,
			}),
		)
	}
	form.reset()
})

chatSocket.onmessage = (e) => {
	let data = JSON.parse(e.data)
	let type = data.type

	if (type == "chat_message") {
		let messages = document.getElementById("messages")
		messages.insertAdjacentHTML(
			"afterbegin",
			`
			<div class="flex items-start">
				<div class="mr-3 text-sm bg-indigo-100 py-2 px-4 shadow rounded-xl">
					<div>
						[CHAT] <span class="font-bold">${data.username}</span> ${data.message}
					</div>
				</div>
			</div>
		`,
		)

	} else if (type == "player_exited") {
		let userScoreboardName = document.getElementById(`${data.username}-username`)
		userScoreboardName.innerHTML = `${data.username} <span class="text-xs"> <br>(Left the room)</span>`
		userScoreboardName.classList.add('text-red-600')
		sendGameUpdates(updatesContainer, data.username, 'has left the room!', 'bg-slate-300')
	} else if (type == "player_entered") {
		let userScoreboardName = document.getElementById(`${data.username}-username`)
		if (userScoreboardName == null) {
			scoreboard.insertAdjacentHTML(
				"beforeend",
				`
				<div id="${data.username}-scoreboard" class="border-2 border-black rounded-lg px-10 py-5 bg-yellow-100">
				<p id="${data.username}-username" class="font-bold text-xl">${data.username}</p>
				<p class="text-center text-sm"><span id="${data.username}-score" class="text-4xl text-justify">${data.player_score}</span> points</p>
      	</div>
				`,
			)
		} else {
			userScoreboardName.innerHTML = `${data.username}`
			userScoreboardName.classList.remove('text-red-600')
		}
		sendGameUpdates(updatesContainer, data.username, 'has entered the room!', 'bg-blue-100')
	} else if (type == 'guess') {
		
		let userScore = document.getElementById(`${data.username}-score`)
		let message = ''
		let color = ''
		if (data.result == true){
			let tile = document.getElementById(data.tile)
			if (currentUser.innerHTML != data.username){
				if (tile.classList.contains("bg-red-100") || tile.classList.contains("bg-yellow-100")) {
					tile.classList.remove("bg-red-100", "bg-yellow-100")
					tile.classList.add("bg-yellow-100")
				}
			}
			let zeroIndexTileArray = tile.id.split('x')
			let [xCord, yCord] = zeroIndexTileArray
			message = `has guessed ${parseInt(xCord)+ 1 }x${parseInt(yCord) + 1} correct! Total points up to: ${data.score}`
			color = 'bg-green-100'
			sendGameUpdates(updatesContainer, data.username, message, color)

			if (data.tiles_left == 0) {
				finishedBanner.insertAdjacentHTML(
					"afterbegin",
					`<h1 class='text-2xl text-center py-5 bg-green-200 w-[80%] mx-auto rounded-lg'>Game is finished! The winner is ${data.username} </h1>`
				)
				buttons.forEach((button) => {
					button.disabled = true
					button.classList.add("disabled", "hover:cursor-not-allowed")
					button.classList.remove('bg-green-100')
				})
			}

		} else if (data.result == false) {
			message = `has guessed a tile wrong! Total points down to: ${data.score} points`
			color = 'bg-red-100'
			sendGameUpdates(updatesContainer, data.username, message, color)
		}
		userScore.innerHTML = `${data.score}`	
	}
}

buttons.forEach(button => {
  button.addEventListener('click', async (e) => {
    let selected = document.querySelector('.bg-blue-300')
    
    if (selected != null) {
      tileId = selected.id
      let [col, row] = tileId.split('x')
      tileCheckUrl = `http://${window.location.host}/check_tile/${roomName}/${col}/${row}/${e.target.innerHTML}`
      const response = await fetch(tileCheckUrl);
      const result = await response.json();

      if (result.result == true){
				selected.innerHTML = e.target.innerHTML
				selected.classList.remove('bg-red-100', 'bg-yellow-100', 'bg-blue-300')
				selected.classList.add('bg-green-100')
      } else if (result.result == false) {
				finishedBanner.innerHTML = ""
				finishedBanner.insertAdjacentHTML(
					"afterbegin",
					`<h1 id='${tileId}-guess' class='lg:text-2xl text-center text-white mt-1 py-2 bg-red-500 w-[95%] lg:w-[80%] mx-auto rounded-lg'>That\'s wrong you lose 10 points for that!</h1>`,
				)
				setTimeout(() => {
					let notification = document.getElementById(`${tileId}-guess`)
					finishedBanner.innerHTML= ''
				}, 3000)
      }
			chatSocket.send(JSON.stringify({
				'type' : 'guess',
				'result' : result.result,
				'username': result.username,
				'tile': tileId,
				'score': result.score,
				'tiles_left': result.tiles_left,
			}))
    }
  }  
)})

function sendGameUpdates(container, username, message, color){

	let htmlText = 
	`
	<div class="flex items-start">
		<div class="mr-3 text-sm ${color} py-2 px-4 shadow rounded-xl">
			<div>
				<span class="font-bold">${username}</span> ${message}
			</div>
		</div>
	</div>
	`

	container.insertAdjacentHTML("afterbegin", htmlText)

}