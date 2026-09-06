(function (global) {
  'use strict';

  // Particle fill-in-the-blank quiz data. Each sentence has one particle
  // blanked out; the multiple-choice quiz in app.js offers the correct
  // particle plus distractors drawn from PARTICLE_DISTRACTOR_GROUPS below.
  //
  // Sentences use inline `kanji[reading]` markup (e.g. "学生[がくせい]")
  // instead of hand-written <ruby> tags — parseFurigana() expands that into
  // ruby HTML for furigana-on display and strips it to plain text for
  // furigana-off display, so every sentence is written once.
  function parseFurigana(text) {
    const html = text.replace(/([一-鿿]+)\[([^\]]+)\]/g, '<ruby>$1<rp>(</rp><rt>$2</rt><rp>)</rp></ruby>');
    const plain = text.replace(/([一-鿿]+)\[([^\]]+)\]/g, '$1');
    return { html, plain };
  }

  // Order they appear as toggles on the setup screen.
  global.PARTICLE_LIST = ['は', 'が', 'を', 'に', 'で', 'へ', 'と', 'も', 'の', 'や'];

  global.PARTICLE_ROMAJI = {
    'は': 'wa', 'が': 'ga', 'を': 'o', 'に': 'ni', 'で': 'de',
    'へ': 'e', 'と': 'to', 'も': 'mo', 'の': 'no', 'や': 'ya',
  };

  // Plausible-but-wrong choices for each particle — picked so none of them
  // would also be grammatically correct in that particle's own sentences
  // below, so every question has exactly one right answer.
  global.PARTICLE_DISTRACTOR_GROUPS = {
    'は': ['が', 'も', 'の'],
    'が': ['は', 'を', 'の'],
    'を': ['が', 'に', 'で'],
    'に': ['で', 'へ', 'と'],
    'で': ['に', 'へ', 'と'],
    'へ': ['で', 'と', 'も'],
    'と': ['や', 'に', 'も'],
    'も': ['は', 'が', 'と'],
    'の': ['が', 'は', 'と'],
    'や': ['と', 'も', 'の'],
  };

  const RAW_ITEMS = [
    // は — topic marker
    { id: 'wa1', particle: 'は', before: '私[わたし]', after: '学生[がくせい]です。', en: 'I am a student.' },
    { id: 'wa2', particle: 'は', before: 'これ', after: '私[わたし]の傘[かさ]です。', en: 'This is my umbrella.' },
    { id: 'wa3', particle: 'は', before: '田中[たなか]さん', after: '先生[せんせい]です。', en: 'Mr. Tanaka is a teacher.' },
    { id: 'wa4', particle: 'は', before: '今日[きょう]', after: '晴[は]れです。', en: 'Today is sunny.' },
    { id: 'wa5', particle: 'は', before: '日本語[にほんご]', after: '難[むずか]しいです。', en: 'Japanese is difficult.' },
    { id: 'wa6', particle: 'は', before: 'この本[ほん]', after: '面白[おもしろ]いです。', en: 'This book is interesting.' },

    // が — subject marker (existence, ability/desire, new information)
    { id: 'ga1', particle: 'が', before: '誰[だれ]', after: '来[き]ましたか。', en: 'Who came?' },
    { id: 'ga2', particle: 'が', before: '猫[ねこ]', after: 'います。', en: 'There is a cat.' },
    { id: 'ga3', particle: 'が', before: '水[みず]', after: '飲[の]みたいです。', en: 'I want to drink water.' },
    { id: 'ga4', particle: 'が', before: '日本語[にほんご]', after: 'わかります。', en: 'I understand Japanese.' },
    { id: 'ga5', particle: 'が', before: '山田[やまだ]さんは車[くるま]', after: 'あります。', en: 'Mr. Yamada has a car.' },
    { id: 'ga6', particle: 'が', before: '頭[あたま]', after: '痛[いた]いです。', en: 'My head hurts.' },

    // を — direct object marker
    { id: 'wo1', particle: 'を', before: 'パン', after: '食[た]べます。', en: 'I eat bread.' },
    { id: 'wo2', particle: 'を', before: '手紙[てがみ]', after: '書[か]きます。', en: 'I write a letter.' },
    { id: 'wo3', particle: 'を', before: '音楽[おんがく]', after: '聞[き]きます。', en: 'I listen to music.' },
    { id: 'wo4', particle: 'を', before: '公園[こうえん]', after: '散歩[さんぽ]します。', en: 'I take a walk through the park.' },
    { id: 'wo5', particle: 'を', before: '新聞[しんぶん]', after: '読[よ]みます。', en: 'I read the newspaper.' },
    { id: 'wo6', particle: 'を', before: '家[いえ]', after: '出[で]ます。', en: 'I leave the house.' },

    // に — time, existence location, target/indirect object, result of change
    { id: 'ni1', particle: 'に', before: '七時[しちじ]', after: '起[お]きます。', en: 'I get up at seven o’clock.' },
    { id: 'ni2', particle: 'に', before: '机[つくえ]の上[うえ]', after: '本[ほん]があります。', en: 'There is a book on the desk.' },
    { id: 'ni3', particle: 'に', before: '友達[ともだち]', after: '電話[でんわ]をかけます。', en: 'I make a phone call to my friend.' },
    { id: 'ni4', particle: 'に', before: '山田[やまだ]さんは先生[せんせい]', after: 'なりました。', en: 'Mr. Yamada became a teacher.' },
    { id: 'ni5', particle: 'に', before: '部屋[へや]', after: '入[はい]ります。', en: 'I enter the room.' },
    { id: 'ni6', particle: 'に', before: '誕生日[たんじょうび]', after: 'プレゼントをもらいました。', en: 'I received a present for my birthday.' },

    // で — location of action, means, cause, scope
    { id: 'de1', particle: 'で', before: '図書館[としょかん]', after: '勉強[べんきょう]します。', en: 'I study at the library.' },
    { id: 'de2', particle: 'で', before: 'バス', after: '学校[がっこう]に行[い]きます。', en: 'I go to school by bus.' },
    { id: 'de3', particle: 'で', before: '日本語[にほんご]', after: '話[はな]します。', en: 'I speak in Japanese.' },
    { id: 'de4', particle: 'で', before: '病気[びょうき]', after: '休[やす]みました。', en: 'I was absent due to illness.' },
    { id: 'de5', particle: 'で', before: '三人[さんにん]', after: 'このケーキを作[つく]りました。', en: 'The three of us made this cake together.' },
    { id: 'de6', particle: 'で', before: 'ペン', after: '名前[なまえ]を書[か]きます。', en: 'I write my name with a pen.' },

    // へ — direction of movement
    { id: 'e1', particle: 'へ', before: '明日[あした]、東京[とうきょう]', after: '行[い]きます。', en: 'Tomorrow, I will go to Tokyo.' },
    { id: 'e2', particle: 'へ', before: '田中[たなか]さんはアメリカ', after: '帰[かえ]ります。', en: 'Mr. Tanaka will return to America.' },
    { id: 'e3', particle: 'へ', before: '鳥[とり]が南[みなみ]', after: '飛[と]んで行[い]きます。', en: 'The birds fly off to the south.' },
    { id: 'e4', particle: 'へ', before: '私[わたし]たちは駅[えき]', after: '向[む]かいました。', en: 'We headed toward the station.' },
    { id: 'e5', particle: 'へ', before: '電車[でんしゃ]は大阪[おおさか]', after: '進[すす]みます。', en: 'The train advances toward Osaka.' },
    { id: 'e6', particle: 'へ', before: '来週[らいしゅう]、京都[きょうと]', after: '旅行[りょこう]に行[い]きます。', en: 'Next week, I’m going on a trip to Kyoto.' },

    // と — accompaniment ("with"), exhaustive listing ("and")
    { id: 'to1', particle: 'と', before: '友達[ともだち]', after: '映画[えいが]を見[み]ました。', en: 'I watched a movie with my friend.' },
    { id: 'to2', particle: 'と', before: '毎朝[まいあさ]、コーヒー', after: 'パンを食[た]べます。', en: 'I eat coffee and bread every morning.' },
    { id: 'to3', particle: 'と', before: '山田[やまだ]さんはお姉[ねえ]さん', after: '住[す]んでいます。', en: 'Ms. Yamada lives with her older sister.' },
    { id: 'to4', particle: 'と', before: '弟[おとうと]', after: 'テニスをしました。', en: 'I played tennis with my younger brother.' },
    { id: 'to5', particle: 'と', before: 'これ', after: 'それは同[おな]じです。', en: 'This and that are the same.' },
    { id: 'to6', particle: 'と', before: '母[はは]', after: '相談[そうだん]しました。', en: 'I consulted with my mother.' },

    // も — "also / too"
    { id: 'mo1', particle: 'も', before: '山田[やまだ]さん', after: '学生[がくせい]です。', en: 'Mr. Yamada is also a student.' },
    { id: 'mo2', particle: 'も', before: '私[わたし]はりんご', after: '好[す]きです。', en: 'I like apples too.' },
    { id: 'mo3', particle: 'も', before: 'これ', after: 'いいですね。', en: 'This one is good too.' },
    { id: 'mo4', particle: 'も', before: '田中[たなか]さん', after: 'パーティーに来[き]ます。', en: 'Mr. Tanaka is also coming to the party.' },
    { id: 'mo5', particle: 'も', before: '弟[おとうと]', after: '日本語[にほんご]を勉強[べんきょう]しています。', en: 'My younger brother is also studying Japanese.' },
    { id: 'mo6', particle: 'も', before: '今日[きょう]', after: '雨[あめ]です。', en: 'Today is rainy too.' },

    // の — possessive / noun modifier
    { id: 'no1', particle: 'の', before: 'これは私[わたし]', after: '本[ほん]です。', en: 'This is my book.' },
    { id: 'no2', particle: 'の', before: '山田[やまだ]さん', after: '傘[かさ]はどこですか。', en: 'Where is Mr. Yamada’s umbrella?' },
    { id: 'no3', particle: 'の', before: '日本語[にほんご]', after: '先生[せんせい]は親切[しんせつ]です。', en: 'The Japanese teacher is kind.' },
    { id: 'no4', particle: 'の', before: 'これは友達[ともだち]', after: '車[くるま]です。', en: 'This is my friend’s car.' },
    { id: 'no5', particle: 'の', before: '東京[とうきょう]', after: '天気[てんき]はいいです。', en: 'Tokyo’s weather is nice.' },
    { id: 'no6', particle: 'の', before: '私[わたし]', after: '家族[かぞく]は四人[よにん]です。', en: 'My family is four people.' },

    // や — non-exhaustive listing ("A や B (など)")
    { id: 'ya1', particle: 'や', before: '机[つくえ]の上[うえ]に本[ほん]', after: 'ペンがあります。', en: 'There are things like a book and a pen on the desk.' },
    { id: 'ya2', particle: 'や', before: '私[わたし]は犬[いぬ]', after: '猫[ねこ]が好[す]きです。', en: 'I like animals like dogs and cats.' },
    { id: 'ya3', particle: 'や', before: '冷蔵庫[れいぞうこ]にりんご', after: '牛乳[ぎゅうにゅう]があります。', en: 'There’s stuff like apples and milk in the fridge.' },
    { id: 'ya4', particle: 'や', before: '部屋[へや]にテレビ', after: '椅子[いす]があります。', en: 'There are things like a TV and a chair in the room.' },
    { id: 'ya5', particle: 'や', before: '週末[しゅうまつ]は買[か]い物[もの]', after: '映画[えいが]を見[み]ます。', en: 'On weekends I do things like shopping and watching movies.' },
    { id: 'ya6', particle: 'や', before: '教室[きょうしつ]に学生[がくせい]', after: '先生[せんせい]がいます。', en: 'There are students and teachers in the classroom.' },
  ];

  global.PARTICLE_QUIZ_ITEMS = RAW_ITEMS.map(item => {
    const before = parseFurigana(item.before);
    const after = parseFurigana(item.after);
    return {
      id: item.id,
      particle: item.particle,
      en: item.en,
      beforePlain: before.plain,
      beforeHtml: before.html,
      afterPlain: after.plain,
      afterHtml: after.html,
    };
  });

})(window);
