# excecss_mortality
- 日本でのCOVID-19による月ごとの超過死亡を都道府県別に、自治体ごとに計算します。  
- python3でコーディングしています。  
- 経験不足の初心者がコーディングしているので、スクリプトに過不足があり、また設計思想にも揺れがあります。  
- ご意見、ご提案を歓迎します。  
## カバーできている都道府県  
本プロジェクトは開発進行中であり、都道府県ごとにデータセットおよび対応するスクリプトを作成しています。超過死亡が計算できる自治体（都道府県及び市町村）は、現在のところ以下の都道府県内のものに限られます（都道府県は順次追加されます）。  
### 北海道および東北  
### 関東
- 千葉県
- 埼玉県
- 東京都
- 神奈川県  
### 中部
- 愛知県
### 近畿
- 京都府
- 大阪府
- 兵庫県
### 中国  
### 四国  
### 九州および沖縄  
## 動作の要件  
- このシステムのコーディングには、python3.8、pycharm2020.2を使用しています。
- このシステムはwindows10で動作を確認しています。パス、文字コードの取り扱いもwindowsを前提としたものになっています。 
- このシステムはメッセージや出力結果、コメントに日本語を使用しています。
## システムの概要
システムは必要なデータが準備されていることを前提に、４つの段階で作動します。それぞれの段階では最初の手順でユーザーによるファイルの選択が必要とされます。また、各段階では最後にファイルを出力します。  
### 0. データの準備  
このシステムに入力するデータは、以下の条件を満たす死亡数のデータである必要があります。  
　1. 都道府県単位でまとめられたものであること  
　2. 市町村別のデータであること  
　3. 月ごとのデータであること  
そこでまず、この条件を満たすデータを集めます（各都道府県のサイトを「人口の推計」「人口動態」などのキーワードで検索すると見つかることが多いです）。データは各月毎のファイルであることが多いですが、月ごとのデータが年単位等でまとめられたファイルであっても問題なく、両者が混在しても計算可能です（大都市では、混在している場合が多いです）。  
データは2012年から最新までのものが必要ですが、これ以前のデータも入力することができます（サンプルとして、兵庫県のファイルを/sample_rude_data_hyogoに置きました）。  
また、死亡データの期間をカバーする自治体の合併情報も必要となります。
### 1. 自治体の変更情報の整理  
- このシステムでは市町村の合併等の情報を自治体コードで処理しています。現存しない自治体のデータには、現在の自治体のコードが割り当てられます。このため、各都道府県について、計算を開始する前に自治体の合併についての情報をまとめた表を作成する必要があります。市町村合併の情報を提供しているサイト等で検索し、csvファイルを作成します。  
- ファイルには、「事由の日時」「旧自治体名」「変更事由」「新自治体名」「新自治体の自治体コード（空欄）」「都道府県名」が含まれなければなりません。それぞれの情報を列にし、一行目に、"date", "old_city", "event", "city", "code", "pref"という文字を記入します（自治体コードは処理過程で自動的に入力されます）。  
- 自治体変更情報をまとめたファイルは、このリポジトリの「data」フォルダにある都道府県別フォルダの中の「ref」フォルダに置いてあります。参考にご覧ください。
- ファイルができたら、"add_local_g_num.py"ファイルを実行し、指示に従ってcsvファイルを入力してください（複数のファイルを同時に選択することはできません）。
- 不具合がなければ、スクリプトの修正は必要ありません。  
- エラー等によって正しい情報が入力できない場合は、"input_local_g_num.py"ファイルを起動して、手動で入力します。また、"local_g_code.py"ファイルを起動すると、市町村名を入力したときに出力されるデータを確認することができます。　　
### 2. データファイルの下処理  
この段階では、データファイルの下処理を行います（再度確認しますが、データファイルは市町村単位、月単位での死亡データを含むものでなくてはなりません）。  
データファイルが各ごとのものである場合はこの下処理に続いて第３段階でデータファイルの処理を行います。データファイルが複数の月データの一覧からなる場合は、この段階のあと直ちに第４段階に進み、第３段階はスキップします。  
- 月別のデータの場合、"prefix_excel.py"ファイルのメインセクションの１行目に都道府県名を関数名として（全部小文字で）セットし、実行します（このファイルはmainとして実行されます）。指示に従ってファイルを入力してください（複数のファイルを選択することができます）。スクリプトファイルの名称にかかわらず、データはエクセルファイルでもcsvファイルでも問題ありません。  
- 月別のデータは、複数のスプレッシートを含むブック形式であっても問題ありません。ただし、以下の条件を満たさなければなりません。  
1. スプレッドシートの先頭から５行目までに「元号＋年+月（+日、または+現在、または+月中）」の形式で表示される年月データが記載されている。  
2. スプレッドシートの先頭から５行目までに「市町村名」「総数」「死亡」が列名として記入されている（それぞれの文言の下に当該のデータが列挙されていればよく、「列名」という表記は必要ありません）  
3. 上記の条件を満たすスプレッドシートがブックの中に一枚だけ含まれている  
- データが以上の条件を満たす場合は、下処理は必要ありません。第３段階に進んでください。  
- データが以上の条件を満たさず、かつ、処理しようとする都道府県についての計算が以前に行われていなければ、スクリプトの加筆が必要になります。"prefix_excel.py", および"set_pfef.py"に各都道府県用のクラスまたは／および関数を定義してください（その他に修正が必要な場合もあります。ファイルの関数をご参照ください）。  
- 処理が終了すると、スクリプトファイルが置かれているディレクトリに"/data/prefixed"というディレクトリが作成され、そこに年毎にデータをまとめたcsvファイルが置かれます（このファイルは第３段階で使用します）。
- 年毎のデータの場合も"prefix_excel.py"ファイルで処理ができます。二種類のファイルが混在している場合は、main関数１行目のクラス名を「都道府県名2」としてください。  
- 年毎のデータの場合、スクリプトファイルへの加筆が必要な場合は"prefix_excel.py"に加えて、"prefix_tow_columns.py"ファイルにも都道府県ごとの関数を定義します。  
- 年毎のデータの処理が終了すると、スクリプトファイルが置かれているディレクトリに"/data"というディレクトリが作成され、そこにcsvファイルが置かれます（このファイルは第４段階で使用します）。
### 3. データファイルの処理  
この段階では、月別のデータファイルを処理して計算に使用できる形式に変換します（データファイルが年別の場合は、この処理は必要ありません）。  
- "dem_prefix.py"ファイルを起動し、メインセクションの１行目に都道府県名をクラスとして（一文字目のみ大文字で）セットし、実行します。指示に従ってファイルを入力してください（複数のファイルを選択することができます。また、全期間のデータを何回かに分けて処理しても問題ありません）。 
- スクリプトは実行途中にデータ中の月付が連続していないケースを警告します。データの欠損は計算結果をゆがませることがあり、好ましくありません。また、データが12か月分以下である場合も注意を喚起します。いずれの場合も、無視して処理を続行することができます。
- 処理しようとする都道府県についての計算が以前に行われていない場合、スクリプトの加筆が必要になる場合があります。この段階で問題になることが多いのは、「日付データが各月１日でない場合」と「県合計のデータの扱い」です。これらの問題は、"set_pref.py"の県別クラスに関数を定義することで処理できる場合が多いです。  
- 処理が完了すると、"data"ディレクトリに、csvファイルが一個出力されます。
- このファイルには、各行に「自治体名」「人口総数（ダミー）」「死亡数」「年月日」「自治体コード」が記されています。人口総数は今回の計算には使わないため、正確な数値ではありません。また、日付はデータの翌月の初日にそろえられています（たとえば、2012年1月のデータであれば、2012-2-1と表記されます。このずれは第４段階で処理され、結果には影響しません）。このファイルは第４段階で使います。
### 4. 超過死亡の計算  
この段階では、COVID-19による超過死亡を自治体ごとに、月別で計算します。  
- "dem_analyze.py"ファイルを起動し、main関数１行目に都道府県名をクラスとしてセットし、実行します。指示に従ってファイルを入力してください（複数のファイルを選択することができます。また、全期間のデータを何回かに分けて処理しても問題ありません）。　
- 処理中に計算を開始する年についての入力が求められます。データが存在する範囲で、任意の年を４ケタの半角数字で入力してください（月の指定は必要ありません）。なお、東日本大震災によるデータのブレとの関係上、2012年を計算のスタート地点とすることを推奨します。  
- 処理中に計算対象の自治体名を選択することができます。また、全自治体についての計算を選択することもできます。
- スクリプトは実行途中にデータの重複を検出すると重複したデータの削除を提案します。
- 計算が終了すると、スクリプトファイルが置かれているディレクトリに"/result"というディレクトリが作成され、そこに超過死亡が検出された市町村、月のデータを記したcsvファイルが置かれます。  
- 計算が終了すると、スクリプトファイルが置かれているディレクトリに"/result"というディレクトリが作成され、そこに市町村別のデータを記したcsvファイルと、グラフを記したpngファイルが出力されます。グラフのファイルには、各月の死亡数を示す棒グラフと、各月の平均死亡数を示す折れ線グラフ、および超過死亡の閾値を示す折れ線グラフが記されています。  
- 計算のスタート年を変えると、それぞれ異なった名前のディレクトリが作られ、異なった名前のファイルが出力されます。
## システムファイルの著作権及び流布  
- このシステムのファイルは、非営利の目的に限り、自由に改変し、また配布することができます
- このシステムの出力結果は、目的のいかんにかかわらず、自由に使用することができます。また、内容に影響を及ぼさない範囲で編集することもできます。  
- システムの設計と運用には万全を期していますが、不注意による誤りや予測できない誤りが生じる可能性は少なくありません（というより、ほぼ確実に含まれるでしょう）。それらのミスは、あらかじめ防御方法を講じておかない場合、重大な結果をもたらす可能性があります。そのことをあらかじめご了承ください。  
- このシステムの出力結果およびこのシステム自体の利用によって生じたいかなる損害、損失に対しても、制作者は責任を負うことはできません。




