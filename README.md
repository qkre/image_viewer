# image_viewer
올린 파일 : untitled.py(소스코드), untitled.ui(ui코드), stylesheet_untitled.qss(css파일), images/image.jfif(이미지 파일)

QPushButton

1.
버튼마다 objectName이 pushbutton1, pushbutton2 ... pushbutton13 이런 식입니다
각 버튼에 기능을 적용하시려면 def 함수로 기능 구현 하신 후
self.<<button의 objectName>>.clicked.connect(self.<<연결할 함수명>>) 로 연결해주시면 됩니다
더 편한 방법 있으시면 그 방법 사용해주셔도 됩니다.


2. ui상의 버튼 이름 혹은 groupbox 이름 등을 바꾸고 싶다.

예를 들어 QPushbutton중 pushbutton2의 이름을 바꾸고 싶다면
<widget class="QPushButton" name="pushButton2"> 행을 찾아
name을 바꿔주시면 됩니다.

3.  
버튼 아래 "hint" 라는 부분이 있는데 이는 버튼의 기능을 간단히 설명하는 lable 입니다.
필요가 없다면 ui에서 ctrl+f 로 hint를 검색 후 몇 줄 아래의 button name을 보고 위치를 특정한 후

&quot;&gt;hint&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt
에서 hint 부분을 지우거나 내용을 변경해주시면 됩니다.

hint에 "rgb를 hsv로 변환" 이라는 내용을 넣으려면 
&quot;&gt;rgb를 hsv로 변환&lt;/span&gt;&lt;/p&gt;&lt;/body&gt;&lt;/html&gt
라고 변경해주시면 됩니다. 혹시 이해가 안되시면 카톡으로 물어보셔도 괜찮습니다.

4.
slider가 있습니다. 사용하시려면 button처럼 연결하시면 됩니다...만,
slider는 ui 상 object name이 horizontalSlider1, 2 입니다.
사용하지 않으신다면 ui 내에서 지우시면 되고 어려우시다면 저한테 물어보시면 삭제하겠습니다.

5. 전에 회의에서 말한 크기 조정은 ui 내에서는 딱히 구현을 할 부분이 없어서 일단 이미지를 QFrame에
크기를 정해서 넣어두었습니다. 이를 임의로 변경해주셔도 되지만, 주의사항으로 이미지의 크기가 Frame의 크기(551x461)을 크게 넘어간다면
이미지가 버튼을 덮어 버튼 클릭이 되지 않을 수 있으니 최대한 Frame 크기 내에서 이미지 크기를 설정해주시길 바랍니다.

6. css파일은 임의로 제가 연결해두어 디자인을 해놓은 상태입니다. 
object name을 바꾸시면 css파일의 연결도 사라지니 바꾸지 않게 부탁드립니다.
디자인 부분은 추가 원하시면 실시간으로 추가 해드리겠습니다. 의견 카톡으로 남겨주세요.

마지막으로 ui에서 조금 더 화려하고 예쁜 느낌이 들게 꾸며보고 싶었으나...
일반 사용자가 아닌 회사에서 사용하는 프로그램이다 보니까 그냥 깔끔하게 하는게 낫겠다 싶어
이미 하던 작업을 다 엎고 새로 만들어 봤습니다..
저도 막 만족하거나 하진 않지만 일단은 기능 추가를 하고 나서 마지막으로 수정해도 되니까 
꼭 이 ui 를 사용하시지 않더라도 일단! 기능과의 연결을 최우선으로 진행하면 좋을 것 같습니다.
모두 방학 중에도 고생 많으십니다!!
