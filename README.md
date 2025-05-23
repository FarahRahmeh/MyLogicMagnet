# Logic Magnet Game Solver 🔎
A puzzle game solver using various search algorithms (BFS, DFS, UCS, Hill Climbing, A*)

# توصيف الحالة (State Representation)

الحالة تمثل الرقعة الحالية التي تم الوصول إليها بعد تنفيذ حركة، وتتكون من خلايا موزعة بإحداثيات معينة ضمن حدود محددة للرقعة. هناك ثمانية أنواع مختلفة من الخلايا، وهي:

- **Out**: خلية خارجية (🔳)
- **Space**: مساحة فارغة (⚫)
- **Iron**: حديد (🔵)
- **White**: أبيض (⚪)
- **Red**: أحمر (🔴)
- **Purple**: بنفسجي (🟣)
- **WhiteIron**: أبيض حديدي (🔘)
- **WhiteRed**: أبيض أحمر (🟥)
- **WhitePurple**: أبيض بنفسجي (🟪)

## الحالة الابتدائية

في البداية، يتم عرض قائمة بالرقع المتاحة ليختار المستخدم منها. كل رقعة عبارة عن شبكة من الخلايا، لكل خلية نوع محدد وموقع (x, y)، ويتم التعامل معها بناءً على موقعها ونوعها.

## العمليات والإجراءات

- **play**: تبدأ عملية اللعب من هذه الدالة، حيث يتلقى المستخدم تعليماته وتستمر اللعبة ما لم يتم الوصول إلى الحالة النهائية.
  
- **getUserMove**: تتحقق من إحداثيات ونوع المغناطيس المدخل من قبل المستخدم، وتتأكد من أن الحركة صالحة.

- **checkMove**: تحدد الخلية المستهدفة التي يُراد التحرك إليها، وتغيّر نوع الخلية السابقة والخلية المستهدفة استنادًا إلى نوع الحركة. تستدعي إجراءات التنافر أو التجاذب بناءً على نوع المغناطيس.

- **checkRepelOrAttract**: تتحقق من نوع المغناطيس المستخدم وتحدد إذا كانت الخلايا المحيطة في الصف والعمود تحتاج إلى جذب أو تنافر.

- **repelMagnet**: تستعرض الصف والعمود للمغناطيس البنفسجي وتنفذ عمليات التنافر والدمج مع الخلايا المجاورة بناءً على نوعها وموقعها باستخدام الإجراء **repelCell**.

- **attractMagnet**: تستعرض الصف والعمود للمغناطيس الأحمر وتنفذ عمليات التجاذب والدمج مع الخلايا المجاورة بناءً على نوعها وموقعها باستخدام الإجراء **pullCell**.

- **checkSuccess**: تتحقق من إذا كانت الرقعة قد وصلت إلى الحالة النهائية، وهي حالة خالية من الخلايا البيضاء.

## الحالة النهائية

الحالة النهائية هي رقعة لا تحتوي على أي خلية بيضاء، مما يعني أنه تم دمج جميع المغناطيسات والقطع الحديدية مع الخلايا البيضاء بالكامل.

## BFS و DFS

### BFS (البحث بالعرض)

يتم تنفيذ الحل باستخدام الإجرائيتين **bfs_play** و **bfs_solver**. تعتمد على بنية معطيات **queue** (باستخدام **deque** من مكتبة بايثون)، حيث يتم تخزين كل حالة حالية مع المسار الذي أوصل إليها. يتم إضافة الحالات الجديدة في نهاية القائمة (**queue**) وإزالة الحالات المستكشفة من مقدمتها بناءً على مبدأ **FIFO** (الأول دخولًا هو الأول خروجًا). بنية البيانات **visited** هي مجموعة **set** تُستخدم لتخزين الحالات التي تمت زيارتها سابقًا لتجنب التكرار.

### DFS (البحث بالعمق)

يتم تنفيذ الحل باستخدام الإجرائيتين **dfs_play** و **dfs_solver**. تعتمد على بنية معطيات **stack** حيث يتم تخزين كل حالة حالية مع المسار الذي أوصل إليها. يتم إضافة الحالات الجديدة في نهاية المكدس (**stack**) وإزالة الحالات المستكشفة من نهايته أيضًا وفق مبدأ **LIFO** (الأخير دخولًا هو الأول خروجًا). تُستخدم **visited** لتخزين الحالات المزارة وتجنب تكرارها.

## آلية الحل في BFS و DFS

الآلية الأساسية لحل المسألة متشابهة في كلتا الخوارزميتين، وتكمن الفروقات الأساسية في بنية المعطيات المستخدمة فقط:

1. **بدء الحل**: يبدأ من الحالة الابتدائية مع مسار فارغ.
2. **التكرار باستخدام queue/stack**:
   - يتم إزالة الحالة الحالية ومسارها من بداية **queue** (في BFS) أو من نهاية **stack** (في DFS).
   - يتم التحقق من كون الحالة النهائية قد تم الوصول إليها باستخدام **checkSuccess**. في حال الوصول للحالة النهائية، تتم طباعة رسالة النجاح ويتم إرجاع المسار الذي يمثل الخطوات المؤدية إلى الحل.
   - إذا كانت الحالة موجودة في **visited**، يتم تجاهلها. إذا لم تكن كذلك، يتم إضافتها إلى **visited**.
3. **استكشاف الحركات الممكنة**:
   - يتم استعراض جميع أنواع المغناطيسات وتحديد إحداثياتها الحالية.
   - تُجرب الحركات الأربعة الممكنة لكل مغناطيس (أعلى، أسفل، يسار، يمين)، مع التأكد من إمكانية التحرك إلى المواقع المستهدفة باستخدام **checkMove**.
   - إذا كانت الحركة صالحة وتعطي حالة جديدة لم تتم زيارتها، يتم إنشاء حالة جديدة وإضافتها إلى **queue/stack**.

## الحل النهائي في BFS و DFS

- في حال وصول الخوارزمية إلى الحالة النهائية، تعود بالمسار وتطبع الخطوات اللازمة للوصول للحل مع رسالة نجاح.
- إذا انتهت جميع الحالات في **queue/stack** دون الوصول إلى الحل، تتم طباعة رسالة تشير إلى عدم وجود حل، ويتم إرجاع **None**.

- # UCS (Uniform Cost Search)  

يتم تنفيذ الحل باستخدام الإجرائيتين `ucs_play` و `ucs_solver`. تعتمد على بنية معطيات **priority queue** (باستخدام `heapq` من مكتبة بايثون)، حيث يتم تخزين كل حالة حالية مع المسار الذي أوصل إليها والتكلفة الإجمالية للوصول إليها. يتم إعطاء الأولوية للحالات ذات التكلفة الأقل وفق مبدأ **Dijkstra's algorithm**.  

**بنية البيانات `visited`** هي مجموعة `set` تُستخدم لتخزين الحالات التي تمت زيارتها سابقًا لتجنب التكرار.  

---

## آلية الحل في UCS  

- **بدء الحل:** يبدأ من الحالة الابتدائية مع مسار فارغ وتكلفة صفرية.  
- **التكرار باستخدام priority queue:**  
  - إزالة الحالة ذات التكلفة الأقل من قائمة الأولويات.  
  - التحقق من كون الحالة النهائية قد تم الوصول إليها باستخدام `checkSuccess`.  
  - إذا كانت الحالة موجودة في `visited`, يتم تجاهلها.  
  - **استكشاف الحركات الممكنة:**  
    - لكل حركة صالحة، يتم حساب التكلفة الجديدة (وفي حالة UCS، تكون تكلفة كل حركة = 1).  
    - إضافة الحالات الجديدة إلى قائمة الأولويات مع مسارها المحدث وتكلفتها الجديدة.  

## الناتج النهائي  
- إذا تم الوصول للحل، يُعاد بالمسار مع تكلفة كل خطوة.  
- إذا لم يُعثر على حل، يُطبع رسالة فشل.  


# Hill Climbing 


يتم تنفيذ الحل باستخدام الإجرائيتين `hill_climbing_play` و `hill_climbing_solver`. تعتمد على دالة **heuristic** التي تقوم بحساب عدد الخلايا البيضاء المتبقية في الرقعة. تختار الخوارزمية دائمًا الحركة التي تقلل قيمة الدالة الإرشادية (أي تقلل عدد الخلايا البيضاء).  

## آلية الحل  

- **بدء الحل:** يبدأ من الحالة الابتدائية مع مسار فارغ.  
- **التكرار:**  
  - تقييم الحالة الحالية باستخدام `heuristic`.  
  - توليد جميع الحالات المجاورة (الحركات الممكنة).  
  - اختيار الحركة التي تعطي أفضل تحسن في الدالة الإرشادية.  

## إيقاف الحل  

- إذا لم يتم العثور على حركة أفضل من الحالة الحالية (أي وصل إلى قمة محلية).  
- إذا تم الوصول للحالة النهائية (قيمة الدالة الإرشادية = 0).  

## محدودية الخوارزمية  
- قد تعلق في قمم محلية ولا تضمن الوصول للحل الأمثل.  
- لا تضمن الحل في جميع الحالات.  


# A* Search  
**بحث A***  

تجمع هذه الخوارزمية بين تكلفة المسار الفعلي `g(n)` والقيمة الإرشادية `h(n)` لاختيار أفضل حركة. تستخدم Priority Queue بمعيار التقييم:  
```f(n) = g(n) + h(n)```  
حيث:  
- **`g(n)`**: التكلفة الفعلية للوصول للحالة الحالية.  
- **`h(n)`**: القيمة الإرشادية (عدد الخلايا البيضاء المتبقية).  

## آلية الحل  

- **بدء الحل:** يبدأ من الحالة الابتدائية مع مسار فارغ وتكلفة صفرية.  
- **التكرار:**  
  - اختيار الحالة ذات أقل قيمة `f(n)` من القائمة.  
  - التحقق من الحالة النهائية.  
  - لكل حركة صالحة، يتم حساب:  
    - `g(n)`: التكلفة الفعلية الجديدة،  
    - `h(n)`: القيمة الإرشادية الجديدة،  
    - `f(n) = g(n) + h(n)`.  

## الميزات  
- تضمن الوصول للحل الأمثل إذا كانت `h(n)` متسقة.  
- أكثر كفاءة من UCS في معظم الحالات.  



# كيفية الاستخدام  
## اللعب اليدوي  
```python  
game = Game(initial_state)  
game.play()
```

## الحل التلقائي (اختر الخوارزمية)
```python
# BFS  
game.bfs_play()  

# DFS  
game.dfs_play()  

# UCS  
game.ucs_play()  

# Hill Climbing  
game.hill_climbing_play()  

# A*  
game.a_star_play()
```
