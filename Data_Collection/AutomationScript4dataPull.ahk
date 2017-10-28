 ; open a new tinder window in IE, must have time lag & already okayed sending location
; Run, https://tinder.com
; Send, {f11}

; sleep, 4000 ;(wait 4 seconds) 

Loop, 15
{
	 ;  open an already active Internet explorer window & maximize it
	WinActivate ahk_class IEFrame
	WinMaximize ahk_class IEFrame
	; Send, {f11}
	sleep, 3000 ;(wait 3 seconds) 
	 ; open developer tools
	Send, {f12}

	sleep, 4000 ;(wait 4 seconds)

	 ; activate the area in the developer's tools section and select all 
	SendEvent {Click, 200, 615}

	#IfWinActive https://tinder.com
	Send, ^a
	
	Send, ^c
	 ;  close developer tools for the next run
	sleep, 3000 ;(wait 3 seconds) 
	 ; open developer tools
	Send, {f12}
	
	 ; pull up new profile
	sleep, 2000 ;(wait 2 seconds) 
	Send, {Right}
	
	fileName := "profile"
	
	 ; open notepad session and drop in the new content
	run, notepad.exe C:\Users\Jennifer\Desktop\AutoHotKey\data\%fileName%%A_Index%.html
	sleep, 2000 ;(wait 2 seconds) 
	
	Send, ^v
	
	Send, ^s
	 ; notepad has a fit about some html characters so you must press enter to by pass and then close the application
	; Send, {Enter}
	
	IfWinExist, %fileName%%A_Index%.html - Notepad
	    WinClose ; use the window found above
	
	 Send, {Enter}
}