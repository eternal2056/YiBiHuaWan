//按键精灵 脚本代码
//上一次（判断是否是第一次，第一次时shangyici = 0，不然就是别的数）
shangyici = 0
//创建ReadAllTextFile函数
Function ReadAllTextFile
  //Const ForReading = 1, ForWriting = 2
  //定义fso与f
  Dim fso, f
  //赋值给fso与f，fso好像没用
  Set fso = CreateObject("Scripting.FileSystemObject")
  //f是文件xianzhuang.txt的句柄差不多的东细，1为读取模式
  Set f = fso.OpenTextFile("D:\Study\python_study\waigua\xianzhuang.txt", 1)
  //f.ReadAll是全读
  ReadAllTextFile = f.ReadAll
End Function
//此函数的返回值为 字符串
//用y字符分离，并返回数组
zuobiaoqun = Split(ReadAllTextFile, "y")
//UBound提供此数组的下标总数
xiabiao = UBound(zuobiaoqun, 1)
temp = Split(zuobiaoqun(0), "x")
MoveTo temp(0), temp(1)
//双击并点击不动
LeftDoubleClick 2
LeftDown 1
Delay 100
		
//循环，从1~下标-1，并移动
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
