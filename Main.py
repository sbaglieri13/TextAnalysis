import Analysis
import Preprocessing

text1 = "To bait fish withal: if it will feed nothing else, it will feed my revenge. He hath disgraced me, and hindered me half a million; laughed at my losses, mocked at my gains, scorned my nation, thwarted my bargains, cooled my friends, heated mine enemies; and what's his reason? I am a Jew. Hath not a Jew eyes? hath not a Jew hands, organs, dimensions, senses, affections, passions? fed with the same food, hurt with the same weapons, subject to the same diseases, healed by the same means, warmed and cooled by the same winter and summer, as a Christian is? If you prick us, do we not bleed? if you tickle us, do we not laugh? if you poison us, do we not die? and if you wrong us, shall we not revenge? If we are like you in the rest, we will resemble you in that. If a Jew wrong a Christian, what is his humility? Revenge. If a Christian wrong a Jew, what should his sufferance be by Christian example? Why, revenge. The villany you teach me, I will execute, and it shall go hard but I will better the instruction."
text2 = "You’re an event. In their lives. People go through life doing the same thing over and over, living the same day again and again. It’s what we do. And every now and then, there’s an event. Something that shocks you, or surprises you – doesn’t matter, it’s an event that reminds you that life can still be interesting. It can always throw something at you that – well, in a zillion years you would never expect it. And it becomes a currency, something that sets you apart. And for a few days, you’re the guy that got stuck in the elevator with a Drag Queen. And everyone asks you about it. And you can laugh. And be the centre of attention. Those people that saw you – they’re going to talk about that for a long time."
text3 = "You may see, Lepidus, and henceforth know, It is not Caesar's natural vice to hate Our great competitor: from Alexandria This is the news: he fishes, drinks, and wastes The lamps of night in revel; is not more man-like Than Cleopatra; nor the queen of Ptolemy More womanly than he; hardly gave audience, or Vouchsafed to think he had partners: you shall find there A man who is the abstract of all faults That all men follow."
text4 = "I’m good, thanks."
text5 = "Everything they do -- everything -- ends with a big hug, because Teletubbies love each other very much. “Biiiiiig Huuuuuug!”"
text6 = "So sweet a kiss the golden sun gives not To those fresh morning drops upon the rose, As thy eye-beams, when their fresh rays have smote The night of dew that on my cheeks down flows: Nor shines the silver moon one half so bright Through the transparent bosom of the deep, As doth thy face through tears of mine give light; Thou shinest in every tear that I do weep: No drop but as a coach doth carry thee; So ridest thou triumphing in my woe. Do but behold the tears that swell in me, And they thy glory through my grief will show: But do not love thyself; then thou wilt keep My tears for glasses, and still make me weep. O queen of queens! how far dost thou excel, No thought can think, nor tongue of mortal tell. How shall she know my griefs? I'll drop the paper: Sweet leaves, shade folly. Who is he comes here?"

text = text1
# text = input("Insert text: ")

print("-------------------------------------------")

print("Frase in ingresso: ", text)

print("-------------------------------------------")

print("Test  sentiment_analysis_en")
sentiment_label = Analysis.sentiment_analysis_en(text)
print("Sentiment label: ", sentiment_label)

print("-------------------------------------------")

print("Test  sentiment_analysis_en_for_sentence")
sentiment_label_for_sentence = Analysis.sentiment_analysis_en_for_sentence(text)
print("Sentiment label for sentence: ", sentiment_label_for_sentence)

print("-------------------------------------------")

print("Test preprocessing_en")
list_of_word = Preprocessing.preprocessing_en(text)
print(list_of_word)

print("-------------------------------------------")

print("Test topic_extraction")
Analysis.topic_extraction(text)

print("-------------------------------------------")