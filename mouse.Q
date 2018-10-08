shangyici = 0
Function ReadAllTextFile
  //Const ForReading = 1, ForWriting = 2
  Dim fso, f
  Set fso = CreateObject("Scripting.FileSystemObject")
  Set f = fso.OpenTextFile("D:\Study\python_study\waigua\xianzhuang.txt", 1)
  ReadAllTextFile = f.ReadAll
End Function

zuobiaoqun = Split(ReadAllTextFile, "y")
xiabiao = UBound(zuobiaoqun, 1)
temp = Split(zuobiaoqun(0), "x")
MoveTo temp(0), temp(1)
LeftDoubleClick 2
LeftDown 1
Delay 100
		
For i=1 To xiabiao-1
TracePrint zuobiaoqun(i)
temp = Split(zuobiaoqun(i), "x")
MoveTo temp(0), temp(1)
Delay 100
Next
shangyici = ReadAllTextFile
Delay 2000
MoveTo 298,787
LeftDoubleClick 2
MoveTo 298,787
LeftDoubleClick 2
MoveTo 0, 0
GetColor = GetPixelColor(426, 524)
If GetColor = "00DDAB" Then 
	Delay 1000
	MoveTo 426, 524
	Delay 200
	LeftDoubleClick 2
	Delay 1000
	MoveTo 132, 254
	LeftDoubleClick 2
	Delay 2000
End If



//当循环条件成立的时候，反复执行循环体


If shangyici <> "0" Then 
	
	While True
		If ReadAllTextFile <> shangyici Then 
			ReadAllTextFile
			zuobiaoqun = Split(ReadAllTextFile, "y")
			xiabiao = UBound(zuobiaoqun, 1)
			temp = Split(zuobiaoqun(0), "x")
			MoveTo temp(0), temp(1)
			LeftDoubleClick 2
			LeftDown 1
			Delay 100
			
			For i=1 To xiabiao-1
			TracePrint zuobiaoqun(i)
			temp = Split(zuobiaoqun(i), "x")
			MoveTo temp(0), temp(1)
			Delay 100
			Next
			shangyici = ReadAllTextFile
			Delay 2000
			MoveTo 298,787
			LeftDoubleClick 2
			MoveTo 298,787
			LeftDoubleClick 2
			MoveTo 0, 0
			GetColor = GetPixelColor(426, 524)
			If GetColor = "00DDAB" Then 
				Delay 4000
				MoveTo 426, 524
				Delay 200
				LeftDoubleClick 2
				Delay 1000
				MoveTo 132, 254
				LeftDoubleClick 2
				Delay 2000
			End If
		End If
	Wend
	
End If
