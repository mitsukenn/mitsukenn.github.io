/**
 * AI用語辞典（/ai-yougo/）のデータ。
 *
 * 方針（AI用語シリーズ_戦略とコラム構造設計_ver1.0.md）:
 * - def は必ず「◯◯とは、〜のことです。」の断定形で始める（AIに引用されやすい形）
 * - use は「で、うちに関係あるの？」への1行の答え。書けるものだけでよい
 * - hot: true は2026年になって急に聞くようになった語（バッジ表示）
 * - link: 該当の解説記事ができたらここに足す。辞典が記事のハブになる
 *
 * 年1回、全面的に見直す（用語の意味は変わる。特にエージェント周辺）。
 */

export type GlossaryTerm = {
  /** アンカーID。/ai-yougo/#rag のように直接指せるようにする */
  id: string;
  /** 日本語の見出し語 */
  term: string;
  /** 英語表記・略語（あれば） */
  en?: string;
  /** 定義。断定形の1〜2文 */
  def: string;
  /** 中小企業にとっての意味。1文 */
  use?: string;
  /** 2026年の注目語 */
  hot?: boolean;
  /** 関連するコラム記事（公開済みのみ） */
  link?: { label: string; href: string };
};

export type GlossaryGroup = {
  id: string;
  name: string;
  lead: string;
  terms: GlossaryTerm[];
};

export const GLOSSARY: GlossaryGroup[] = [
  {
    id: 'basic',
    name: 'きほん・しくみ',
    lead: 'ニュースでよく出てくる、AIの土台にあたる言葉です。',
    terms: [
      {
        id: 'seisei-ai',
        term: '生成AI',
        en: 'Generative AI',
        def: '生成AIとは、文章や画像、音声などを新しく作り出せるAIのことです。決まった答えを探すのではなく、その場で作るところが今までのシステムと違います。',
      },
      {
        id: 'llm',
        term: 'LLM（大規模言語モデル）',
        en: 'Large Language Model',
        def: 'LLMとは、大量の文章を読み込んで言葉のつながり方を学んだAIのことです。ChatGPTやGeminiの中身にあたります。',
        use: 'ニュースで「AI」と呼ばれているものの多くは、実体はこのLLMです。',
      },
      {
        id: 'foundation-model',
        term: '基盤モデル',
        en: 'Foundation Model',
        def: '基盤モデルとは、いろいろな用途の土台になる大きくて汎用的なAIモデルのことです。この上に各社が専用の機能を載せていきます。',
      },
      {
        id: 'slm',
        term: 'SLM（小規模言語モデル）',
        en: 'Small Language Model',
        def: 'SLMとは、動作が軽くて費用も安い小型のAIモデルのことです。手元のパソコンやスマホの中でも動きます。',
        use: 'ぜんぶを賢い大型モデルに任せず、簡単な処理は小型に振ると費用が下がります。',
        hot: true,
      },
      {
        id: 'transformer',
        term: 'トランスフォーマー',
        en: 'Transformer',
        def: 'トランスフォーマーとは、今のAIの中身を支えている基本設計のことです。2017年に発表され、生成AIブームの土台になりました。',
      },
      {
        id: 'attention',
        term: 'アテンション',
        en: 'Attention',
        def: 'アテンションとは、文章のどこに注目すべきかをAIが判断する仕組みのことです。長い文でも話の筋を追えるのは、この仕組みのおかげです。',
      },
      {
        id: 'parameter',
        term: 'パラメータ',
        en: 'Parameter',
        def: 'パラメータとは、AIモデルの規模を表す数字のことです。人間でいう脳細胞の数にあたり、多いほど賢い傾向はありますが、その分お金も時間もかかります。',
      },
      {
        id: 'token',
        term: 'トークン',
        en: 'Token',
        def: 'トークンとは、AIが文章を数えるときの単位のことです。日本語は1文字がおよそ1〜2トークンにあたります。',
        use: 'AIの利用料金はこのトークン数で決まるので、費用の話をするときの共通語になります。',
      },
      {
        id: 'context-window',
        term: 'コンテキストウィンドウ',
        en: 'Context Window',
        def: 'コンテキストウィンドウとは、AIが一度に読み込める情報量の上限のことです。ここを超えると、前に話した内容から順に忘れていきます。',
        use: '会話が長くなるとAIの返事が急に雑になるのは、たいていこれが原因です。',
      },
      {
        id: 'inference',
        term: '推論（インファレンス）',
        en: 'Inference',
        def: '推論とは、学習が済んだAIを実際に動かして答えを出すことです。私たちが普段AIを使っている行為そのものを指します。',
      },
      {
        id: 'pretraining',
        term: '事前学習',
        en: 'Pre-training',
        def: '事前学習とは、大量のデータを読ませてAIの基礎学力を作る工程のことです。ここは開発元がやる作業なので、利用する側が触ることはありません。',
      },
      {
        id: 'finetuning',
        term: 'ファインチューニング',
        en: 'Fine-tuning',
        def: 'ファインチューニングとは、自社のデータを追加で学習させてAIを専用にすることです。費用も手間もかかるので、まずはRAGで足りないかを先に検討します。',
      },
      {
        id: 'distillation',
        term: '蒸留',
        en: 'Distillation',
        def: '蒸留とは、大きなモデルの賢さを小さなモデルに移す技術のことです。安くて速いAIが次々に出てくる理由がこれです。',
      },
      {
        id: 'quantization',
        term: '量子化',
        en: 'Quantization',
        def: '量子化とは、精度をわずかに落としてAIを軽く速く動かす圧縮技術のことです。手元のパソコンでAIを動かすときに使われます。',
      },
      {
        id: 'moe',
        term: 'MoE（混合エキスパート）',
        en: 'Mixture of Experts',
        def: 'MoEとは、巨大なAIの中から必要な専門家の部分だけを動かす構造のことです。賢さを保ったまま計算量を減らせます。',
        hot: true,
      },
      {
        id: 'multimodal',
        term: 'マルチモーダル',
        en: 'Multimodal',
        def: 'マルチモーダルとは、文字・画像・音声・動画をまとめて扱えることです。写真を見せて質問できるのは、この能力によります。',
        use: '手書きの伝票やホワイトボードを撮って渡す、という使い方ができます。',
      },
    ],
  },
  {
    id: 'prompt',
    name: '使いこなし・プロンプト',
    lead: '同じAIでも、頼み方で結果が変わります。その頼み方まわりの言葉です。',
    terms: [
      {
        id: 'prompt',
        term: 'プロンプト',
        en: 'Prompt',
        def: 'プロンプトとは、AIへの指示文のことです。同じAIでも、指示の書き方で結果が大きく変わります。',
        link: { label: 'ChatGPTの始め方', href: '/blog/chatgpt-hajimekata/' },
      },
      {
        id: 'prompt-engineering',
        term: 'プロンプトエンジニアリング',
        en: 'Prompt Engineering',
        def: 'プロンプトエンジニアリングとは、ほしい答えを引き出すために指示文を作り込む工夫のことです。',
        use: '「前提・やってほしいこと・出してほしい形」の3つを書くだけでも、ぐっと良くなります。',
      },
      {
        id: 'system-prompt',
        term: 'システムプロンプト',
        en: 'System Prompt',
        def: 'システムプロンプトとは、AIの役割やルールを裏側で固定しておく指示のことです。社内用のAIを作るときの土台になります。',
      },
      {
        id: 'few-shot',
        term: 'Few-shot（少数事例）',
        en: 'Few-shot Prompting',
        def: 'Few-shotとは、見本をいくつか見せて出力の型をそろえる方法のことです。文体や書式を統一したいときに効きます。',
      },
      {
        id: 'cot',
        term: 'CoT（思考の連鎖）',
        en: 'Chain of Thought',
        def: 'CoTとは、答えを出す前に途中の考えを順番に書かせる方法のことです。計算や条件の多い判断で、間違いが減ります。',
      },
      {
        id: 'reasoning-model',
        term: 'リーズニングモデル（推論特化型）',
        en: 'Reasoning Model',
        def: 'リーズニングモデルとは、答える前にじっくり考えるタイプのAIのことです。難しい問題に強い一方で、遅くて高くつきます。',
        use: '毎日の文章作成には要りません。込み入った判断のときだけ使い分けます。',
        hot: true,
      },
      {
        id: 'test-time-compute',
        term: 'テストタイムコンピュート（思考予算）',
        en: 'Test-time Compute',
        def: 'テストタイムコンピュートとは、考える時間を増やすほどAIが賢くなる、という考え方のことです。用途に応じて「どこまで考えさせるか」を選べるようになってきました。',
        hot: true,
      },
      {
        id: 'temperature',
        term: '温度（Temperature）',
        en: 'Temperature',
        def: '温度とは、AIの出力のブレ幅を決める設定のことです。低くすると堅実に、高くすると発想が広がります。',
      },
      {
        id: 'structured-output',
        term: '構造化出力（JSONモード）',
        en: 'Structured Output',
        def: '構造化出力とは、決まった形式で答えさせて、そのままシステムに流し込める機能のことです。',
        use: 'Excelや基幹システムとAIをつなぐときの要になる部分です。',
      },
      {
        id: 'role-prompt',
        term: 'ロールプロンプト',
        en: 'Role Prompting',
        def: 'ロールプロンプトとは、「あなたは経理担当者です」のようにAIへ役割を与える指示のことです。回答の視点と言葉づかいが変わります。',
      },
      {
        id: 'meta-prompt',
        term: 'メタプロンプト',
        en: 'Meta Prompting',
        def: 'メタプロンプトとは、プロンプトそのものをAIに書かせる方法のことです。',
        use: '指示が思いつかないときは、「いい指示文を考えて」と頼むのが早道です。',
      },
      {
        id: 'context-engineering',
        term: 'コンテキストエンジニアリング',
        en: 'Context Engineering',
        def: 'コンテキストエンジニアリングとは、AIに何を読ませて何を捨てるかを設計することです。指示文の工夫より、こちらのほうが結果を左右するようになってきました。',
        hot: true,
      },
    ],
  },
  {
    id: 'data',
    name: '自社のデータとつなぐ',
    lead: '「うちの事情を分かっているAI」にするための言葉です。',
    terms: [
      {
        id: 'rag',
        term: 'RAG（検索拡張生成）',
        en: 'Retrieval-Augmented Generation',
        def: 'RAGとは、社内の資料を検索してからAIに答えさせる仕組みのことです。AIに自社の事情を分からせる、いちばん現実的な方法です。',
        use: '追加学習より安く、資料を差し替えれば中身もすぐ更新できます。',
      },
      {
        id: 'embedding',
        term: '埋め込み（エンベディング）',
        en: 'Embedding',
        def: '埋め込みとは、文章の意味を数値の並びに変換することです。言葉づかいが違っても、意味が近ければ探し出せるようになります。',
      },
      {
        id: 'vector-db',
        term: 'ベクトルデータベース',
        en: 'Vector Database',
        def: 'ベクトルデータベースとは、意味検索のための数値を保管しておく置き場のことです。RAGの裏側で動いています。',
      },
      {
        id: 'chunking',
        term: 'チャンキング',
        en: 'Chunking',
        def: 'チャンキングとは、資料を検索しやすい大きさに切り分ける作業のことです。地味な工程ですが、RAGの精度はここでほぼ決まります。',
      },
      {
        id: 'reranking',
        term: 'リランキング',
        en: 'Reranking',
        def: 'リランキングとは、検索で拾った候補をもう一度並べ替えて、精度を上げる工程のことです。',
      },
      {
        id: 'graphrag',
        term: 'GraphRAG',
        en: 'GraphRAG',
        def: 'GraphRAGとは、知識を「つながり」の形で持たせて、関係をたどれるようにしたRAGのことです。人や案件の関係を追いたい用途に向きます。',
        hot: true,
      },
      {
        id: 'grounding',
        term: 'グラウンディング',
        en: 'Grounding',
        def: 'グラウンディングとは、AIの答えを出典に基づかせて、事実から離れないようにすることです。',
      },
      {
        id: 'knowledge-base',
        term: 'ナレッジベース',
        en: 'Knowledge Base',
        def: 'ナレッジベースとは、AIに読ませる社内知識の置き場のことです。',
        use: 'AI導入でいちばん最初にやることは、たいていここの整理です。',
      },
      {
        id: 'long-context',
        term: 'ロングコンテキスト',
        en: 'Long Context',
        def: 'ロングコンテキストとは、本1冊ぶんのような長い資料を丸ごと読ませる使い方のことです。検索を挟まず全部渡してしまう力技ですが、確実です。',
      },
      {
        id: 'context-compression',
        term: 'コンテキスト圧縮',
        en: 'Context Compression',
        def: 'コンテキスト圧縮とは、長くなった会話を要約して持ち回る技術のことです。',
      },
      {
        id: 'persistent-memory',
        term: '永続メモリ',
        en: 'Persistent Memory',
        def: '永続メモリとは、会話をまたいでAIがこちらのことを覚えておく機能のことです。毎回いちから説明する手間がなくなります。',
        hot: true,
      },
      {
        id: 'synthetic-data',
        term: '合成データ',
        en: 'Synthetic Data',
        def: '合成データとは、AI自身が作った学習用の疑似データのことです。実際のデータが少ない現場で使われます。',
      },
    ],
  },
  {
    id: 'agent',
    name: 'AIエージェント',
    lead: '2026年、いちばん動きが大きいところです。「答えるAI」から「やってくれるAI」へ。',
    terms: [
      {
        id: 'ai-agent',
        term: 'AIエージェント',
        en: 'AI Agent',
        def: 'AIエージェントとは、目的を渡すと手順を自分で考えて実行するAIのことです。「聞いたら答える」から「代わりにやっておく」への変化です。',
        use: '人を増やせない会社にとって、いちばん影響が大きい変化です。',
        hot: true,
        link: { label: 'ChatGPTは使えるのに、仕事が減らない', href: '/blog/chatgpt-shigoto-herananai/' },
      },
      {
        id: 'agentic-ai',
        term: 'エージェンティックAI',
        en: 'Agentic AI',
        def: 'エージェンティックAIとは、AIが自律的に仕事を進める流れ全体を指す言葉です。2026年のAI業界でいちばん語られている領域です。',
        hot: true,
      },
      {
        id: 'function-calling',
        term: 'Function Calling（ツール利用）',
        en: 'Function Calling',
        def: 'Function Callingとは、AIが外部の機能やソフトを自分で呼び出すことです。計算・検索・メール送信などを任せられるようになります。',
      },
      {
        id: 'mcp',
        term: 'MCP（モデルコンテキストプロトコル）',
        en: 'Model Context Protocol',
        def: 'MCPとは、AIと社内のツールやデータをつなぐための共通規格のことです。対応するソフトが増えるほど、AIにできる仕事が増えます。',
        use: 'いま使っている業務ソフトがMCPに対応するかどうかは、確認しておく価値があります。',
        hot: true,
      },
      {
        id: 'a2a',
        term: 'A2A（エージェント間連携）',
        en: 'Agent to Agent',
        def: 'A2Aとは、AI同士が会話して連携するための規格のことです。担当の違うAIに、仕事を引き継がせられます。',
        hot: true,
      },
      {
        id: 'multi-agent',
        term: 'マルチエージェント',
        en: 'Multi-agent System',
        def: 'マルチエージェントとは、役割の違う複数のAIをチームとして動かす構成のことです。1体に全部やらせるより精度が上がります。',
        hot: true,
      },
      {
        id: 'sub-agent',
        term: 'サブエージェント',
        en: 'Sub-agent',
        def: 'サブエージェントとは、親のAIが子のAIに仕事を振り分ける形のことです。',
      },
      {
        id: 'orchestration',
        term: 'オーケストレーション',
        en: 'Orchestration',
        def: 'オーケストレーションとは、複数のAIや処理の順番を組み立てて、全体を指揮することです。',
      },
      {
        id: 'workflow-vs-autonomous',
        term: 'ワークフロー型と自律型',
        def: 'ワークフロー型と自律型とは、手順を固定するか、AIに任せるかという設計の分かれ道のことです。',
        use: '間違いが許されない業務は手順固定、調べものなどは自律型、と分けるのが現実的です。',
      },
      {
        id: 'hitl',
        term: 'ヒューマン・イン・ザ・ループ',
        en: 'Human in the Loop',
        def: 'ヒューマン・イン・ザ・ループとは、大事な判断のところで人の承認を挟む設計のことです。AIに任せる範囲を、安全に広げるための考え方です。',
      },
      {
        id: 'autonomy-level',
        term: '自律度（オートノミーレベル）',
        en: 'Autonomy Level',
        def: '自律度とは、どこまでをAIに任せるかの段階設定のことです。提案だけ／下書きまで／実行まで、と分けて決めます。',
        use: '導入で揉めるのは、たいていここを決めていないからです。',
        hot: true,
      },
      {
        id: 'computer-use',
        term: 'コンピュータユース',
        en: 'Computer Use',
        def: 'コンピュータユースとは、AIがマウスとキーボードを使ってパソコンを直接操作する機能のことです。連携用の窓口がない古いソフトも動かせます。',
        hot: true,
      },
      {
        id: 'browser-agent',
        term: 'ブラウザエージェント',
        en: 'Browser Agent',
        def: 'ブラウザエージェントとは、Webサイトを自分で見て回って作業するAIのことです。調べもの・申し込み・比較などを任せられます。',
        hot: true,
      },
      {
        id: 'vibe-coding',
        term: 'バイブコーディング',
        en: 'Vibe Coding',
        def: 'バイブコーディングとは、話し言葉で「こんな感じ」と伝えて、AIにソフトを作らせる開発の仕方のことです。',
        use: '小さな社内ツールなら、この作り方で十分に実用になります。',
        hot: true,
        link: { label: '自社専用AIアプリは何がどこまで作れるのか', href: '/blog/ai-app-nani-ga-ikura/' },
      },
      {
        id: 'coding-agent',
        term: 'コーディングエージェント',
        en: 'Coding Agent',
        def: 'コーディングエージェントとは、自分でコードを書き、動かし、直すところまでやるAIのことです。',
        hot: true,
        link: { label: 'ChatGPT・Claude Code・Codexの違い', href: '/blog/chatgpt-claude-code-codex-chigai/' },
      },
      {
        id: 'guardrail',
        term: 'ガードレール',
        en: 'Guardrail',
        def: 'ガードレールとは、AIがやってはいけないことをあらかじめ制限しておく仕掛けのことです。',
      },
    ],
  },
  {
    id: 'ops',
    name: '導入と運用',
    lead: '実際に業務へ入れるとき、費用や運用の話で出てくる言葉です。',
    terms: [
      {
        id: 'api',
        term: 'API',
        en: 'API',
        def: 'APIとは、自社のシステムからAIを呼び出すための窓口のことです。画面を開かなくても、業務の流れの中にAIを組み込めます。',
      },
      {
        id: 'pay-as-you-go',
        term: '従量課金・トークン単価',
        def: '従量課金とは、使ったぶんだけ支払うAIの料金体系のことです。',
        use: '月額固定と違って使い方で費用が動くので、上限設定の有無を必ず確認します。',
      },
      {
        id: 'prompt-cache',
        term: 'プロンプトキャッシュ',
        en: 'Prompt Caching',
        def: 'プロンプトキャッシュとは、毎回同じ前置きを使い回して料金と待ち時間を減らす仕組みのことです。',
      },
      {
        id: 'latency',
        term: 'レイテンシ・ストリーミング',
        def: 'レイテンシとは応答までの待ち時間、ストリーミングとは答えが少しずつ表示される仕組みのことです。使い心地を大きく左右します。',
      },
      {
        id: 'llmops',
        term: 'LLMOps',
        en: 'LLMOps',
        def: 'LLMOpsとは、生成AIを本番で運用し、改善し続けるための仕組みづくりのことです。',
      },
      {
        id: 'eval',
        term: '評価（Eval）・LLM-as-a-Judge',
        def: '評価とは、AIの出力品質をテストとして測ることです。その採点自体をAIにさせる方法をLLM-as-a-Judgeと呼びます。',
        use: '「なんとなく良くなった気がする」で終わらせないために要ります。',
        hot: true,
      },
      {
        id: 'observability',
        term: 'オブザーバビリティ（トレーシング）',
        en: 'Observability',
        def: 'オブザーバビリティとは、AIがどう考えて何をしたかを記録して、後から追えるようにすることです。エージェントを実務に入れるなら欠かせません。',
      },
      {
        id: 'model-migration',
        term: 'モデル移行',
        def: 'モデル移行とは、新しいAIモデルへ切り替えるときに品質を検証し直す作業のことです。',
        use: 'モデルは1年で入れ替わります。乗り換える前提で作るのがコツです。',
      },
      {
        id: 'local-llm',
        term: 'ローカルLLM・オンプレミス',
        def: 'ローカルLLMとは、社内のパソコンやサーバーの中でAIを動かす形のことです。データを外に出したくない業種の選択肢になります。',
      },
      {
        id: 'open-weight',
        term: 'オープンウェイトモデル',
        en: 'Open-weight Model',
        def: 'オープンウェイトモデルとは、中身が公開されていて自社に置いて使えるAIのことです。',
      },
      {
        id: 'edge-ai',
        term: 'エッジAI・オンデバイスAI',
        def: 'エッジAIとは、スマホや機器の中でAIが直接動く形のことです。通信が要らず、反応も速くなります。',
        hot: true,
      },
      {
        id: 'ai-gateway',
        term: 'AIゲートウェイ・モデルルーティング',
        def: 'AIゲートウェイとは、用途に応じて最適なAIへ自動で振り分ける仕組みのことです。安いAIと賢いAIを使い分けて費用を抑えます。',
        hot: true,
      },
    ],
  },
  {
    id: 'media',
    name: '画像・動画・音声',
    lead: 'チラシ、写真、ナレーション、電話対応。目と耳に関わるAIです。',
    terms: [
      {
        id: 'text-to-image',
        term: 'テキスト to イメージ',
        en: 'Text to Image',
        def: 'テキスト to イメージとは、文章から画像を作る機能のことです。',
      },
      {
        id: 'diffusion',
        term: '拡散モデル',
        en: 'Diffusion Model',
        def: '拡散モデルとは、ノイズから絵を描き起こしていく画像生成の主流の方式のことです。',
      },
      {
        id: 'inpainting',
        term: 'インペイント（画像編集AI）',
        en: 'Inpainting',
        def: 'インペイントとは、画像の一部だけを差し替えたり修正したりする機能のことです。',
        use: 'チラシの文字だけ直す、商品の背景だけ変える、といった実務で使い出があります。',
      },
      {
        id: 'video-gen',
        term: '動画生成AI',
        def: '動画生成AIとは、文章や写真から動画を作る技術のことです。数秒から数十秒の短い素材づくりが、現実的な使いどころです。',
      },
      {
        id: 'tts',
        term: '音声合成（TTS）・ボイスクローン',
        en: 'Text to Speech',
        def: '音声合成とは文章を読み上げる技術、ボイスクローンとは特定の人の声を再現する技術のことです。',
        use: '電話の自動案内や、動画のナレーションに使えます。',
      },
      {
        id: 'realtime-voice',
        term: 'リアルタイム音声対話',
        def: 'リアルタイム音声対話とは、電話のように途切れずに会話できる音声AIのことです。予約受付や一次対応の自動化が、現実味を帯びてきました。',
        hot: true,
      },
      {
        id: '3d-gen',
        term: '3D生成',
        def: '3D生成とは、写真や文章から3Dモデルを作る技術のことです。',
      },
      {
        id: 'style-reference',
        term: '参照画像・スタイル参照',
        def: '参照画像とは、見本の画像をAIに渡して作風や構図をそろえる方法のことです。',
        use: '同じトーンの素材を何枚も作りたいときは、これが必須です。',
      },
      {
        id: 'upscaling',
        term: 'アップスケーリング',
        en: 'Upscaling',
        def: 'アップスケーリングとは、粗い画像や動画を高精細に作り直す処理のことです。古い写真素材の再利用に使えます。',
      },
      {
        id: 'c2pa',
        term: 'C2PA・電子透かし',
        def: 'C2PAとは、AIで作ったことを画像自身に記録しておく来歴の仕組みのことです。',
        hot: true,
      },
    ],
  },
  {
    id: 'risk',
    name: 'リスクと品質',
    lead: '「怖い」を「気をつけるべき点」に変えるための言葉です。',
    terms: [
      {
        id: 'hallucination',
        term: 'ハルシネーション',
        en: 'Hallucination',
        def: 'ハルシネーションとは、AIが事実でないことをもっともらしく答えてしまう現象のことです。',
        use: 'なくす方法はありません。「誰が確認するか」を決める運用でしのぎます。',
        link: { label: '騙されないAI相談相手の選び方5箇条', href: '/blog/ai-soudan-aite-erabikata/' },
      },
      {
        id: 'prompt-injection',
        term: 'プロンプトインジェクション',
        en: 'Prompt Injection',
        def: 'プロンプトインジェクションとは、Webページや資料に指示を仕込んでAIを乗っ取る攻撃のことです。AIに外部の情報を読ませるほど、リスクが上がります。',
        hot: true,
      },
      {
        id: 'jailbreak',
        term: 'ジェイルブレイク',
        en: 'Jailbreak',
        def: 'ジェイルブレイクとは、AIにかけられた制限を回避させる不正な指示のことです。',
      },
      {
        id: 'opt-out',
        term: '学習利用オプトアウト',
        def: '学習利用オプトアウトとは、入力したデータをAIの学習に使わせない設定のことです。',
        use: '業務で使うなら、まずここを確認します。法人向けプランは、はじめから使われない設定のことが多いです。',
      },
      {
        id: 'bias',
        term: 'バイアス',
        en: 'Bias',
        def: 'バイアスとは、学習データに含まれる偏りが答えに出てしまうことです。採用や評価に使うときは、特に注意が要ります。',
      },
      {
        id: 'deepfake',
        term: 'ディープフェイク',
        en: 'Deepfake',
        def: 'ディープフェイクとは、本物そっくりに作られた偽の映像や音声のことです。',
        use: '社長の声を装った送金指示のような詐欺が、実際に起きています。',
      },
      {
        id: 'shadow-ai',
        term: 'シャドーAI',
        en: 'Shadow AI',
        def: 'シャドーAIとは、会社が把握しないまま社員が個人のAIを業務に使っている状態のことです。',
        use: '禁止すると隠れて使われます。使ってよい範囲を決めるほうが、結果として安全です。',
        hot: true,
      },
      {
        id: 'copyright',
        term: '著作権（依拠性・類似性）',
        def: '依拠性と類似性とは、AIの生成物が既存の作品に似ていた場合に、権利侵害かどうかを判断する2つの軸のことです。',
      },
      {
        id: 'ai-work-rights',
        term: 'AI生成物の権利帰属',
        def: 'AI生成物の権利帰属とは、AIが作ったものが誰の著作物になるのかという論点のことです。人の創作的な関わりがどれだけあったかで判断されます。',
      },
      {
        id: 'red-teaming',
        term: 'レッドチーミング',
        en: 'Red Teaming',
        def: 'レッドチーミングとは、わざと攻撃をしかけて弱点を先に見つける検証のことです。',
      },
      {
        id: 'alignment',
        term: 'アライメント・RLHF',
        en: 'Alignment / RLHF',
        def: 'アライメントとは、AIを人の意図や価値観に沿わせるための調整のことです。RLHFは、人の評価を使ってそれを行う代表的な手法です。',
      },
    ],
  },
  {
    id: 'biz',
    name: '制度・社会・ビジネス',
    lead: '経営の話をするときに出てくる言葉です。補助金や法律もここ。',
    terms: [
      {
        id: 'ai-guideline',
        term: 'AI事業者ガイドライン',
        def: 'AI事業者ガイドラインとは、国が示しているAIを扱う事業者向けの指針のことです。社内ルールを作るときの下敷きになります。',
      },
      {
        id: 'ai-suishinho',
        term: 'AI推進法（AI新法）',
        def: 'AI推進法とは、日本のAI活用推進を定めた法律のことです。罰則より推進に軸足がある点が、海外の規制と違います。',
        link: { label: '骨太の方針2026を中小企業目線で読む', href: '/blog/honebuto-2026-ax/' },
      },
      {
        id: 'eu-ai-act',
        term: 'EU AI Act',
        def: 'EU AI Actとは、リスクの大きさで規制を段階分けした、EUの包括的なAI法のことです。EUと取引がある会社は影響を受けます。',
      },
      {
        id: 'ai-governance',
        term: 'AIガバナンス・社内利用規程',
        def: 'AIガバナンスとは、誰が何にどう使ってよいかを決めた社内ルールの整備のことです。',
        use: 'A4で1枚あれば十分に機能します。無いまま使い続けるのが、いちばん危ない状態です。',
      },
      {
        id: 'ai-literacy',
        term: 'AIリテラシー',
        def: 'AIリテラシーとは、AIの仕組みと限界を分かったうえで使いこなす力のことです。',
      },
      {
        id: 'geo',
        term: 'GEO・LLMO',
        en: 'Generative Engine Optimization',
        def: 'GEO・LLMOとは、AIに引用してもらうためのサイトの整え方のことです。検索順位ではなく、AIの回答に載ることを狙います。',
        hot: true,
      },
      {
        id: 'ai-search',
        term: 'AI検索・ゼロクリック',
        def: 'ゼロクリックとは、AIが要約で答えてしまい、元のサイトまで人が来なくなる現象のことです。',
        use: '「読まれる」より「引用される」を前提に、情報発信を組み直す必要があります。',
        hot: true,
      },
      {
        id: 'hojokin',
        term: 'デジタル化・AI導入補助金',
        def: 'デジタル化・AI導入補助金とは、中小企業のIT・AI導入を国が支援する制度のことです。旧IT導入補助金にあたります。',
        link: { label: 'デジタル化・AI導入補助金2026まるわかり', href: '/blog/digital-ai-hojokin-2026/' },
      },
      {
        id: 'poc-tsukare',
        term: 'PoC疲れ',
        def: 'PoC疲れとは、試すだけで終わってしまい、本番の導入に至らない状態のことです。',
        use: '「小さくても本番で使う」ところまで決めてから始めるのが、いちばんの対策です。',
        link: { label: 'ChatGPTは使えるのに、仕事が減らない', href: '/blog/chatgpt-shigoto-herananai/' },
      },
      {
        id: 'ax',
        term: 'AX（AIトランスフォーメーション）',
        def: 'AXとは、AIを前提に仕事のやり方そのものを変えることです。DXの次の段階として、国の方針にも入りました。',
        hot: true,
        link: { label: 'AXとは何か', href: '/blog/ax-toha-nani/' },
      },
      {
        id: 'physical-ai',
        term: 'フィジカルAI',
        en: 'Physical AI',
        def: 'フィジカルAIとは、ロボットや設備を動かす、現実世界で働くAIのことです。製造や建設の現場で実用が始まっています。',
        hot: true,
      },
    ],
  },
];

/** 全用語をひとつの配列で取り出す（構造化データ・件数表示用） */
export const ALL_TERMS: GlossaryTerm[] = GLOSSARY.flatMap((g) => g.terms);

/**
 * ページ上部に出す「よく調べられる言葉」。
 * 検索から先頭に着地した人が、スクロールせず1タップで目的の語へ飛べるようにする。
 * 当面は編集部選定。Search Consoleのクエリが貯まったら実データで入れ替える。
 */
const QUICK_IDS = [
  'ai-agent',
  'mcp',
  'rag',
  'hallucination',
  'llm',
  'seisei-ai',
  'token',
  'ax',
  'prompt',
  'vibe-coding',
  'context-window',
  'multimodal',
  'shadow-ai',
  'local-llm',
  'finetuning',
  'reasoning-model',
  'geo',
  'deepfake',
  'hojokin',
  'physical-ai',
] as const;

export const QUICK_TERMS: GlossaryTerm[] = QUICK_IDS.map((id) => {
  const t = ALL_TERMS.find((x) => x.id === id);
  if (!t) throw new Error(`QUICK_IDS に存在しない用語IDがあります: ${id}`);
  return t;
});
