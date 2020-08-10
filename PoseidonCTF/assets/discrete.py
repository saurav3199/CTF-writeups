from gmpy2 import *
from Crypto.Util.number import isPrime, getPrime, getRandomRange, bytes_to_long, long_to_bytes
g = 172749132303451034825184289722866887646478207718904031630914096520683022158034517117605936723970812800902379716660696042889559048647206589145869496198395421965440272135852383965230458163451729744948637995163776071512309614027603968693250321092562108610034043037860044795655266224453184735452048413623769098671844195106558284409006269382544367448145088128499405797694142037310933061698125568790497068516077791616445318819525778890129259953967830407023305805724947609041398183006524760589480514375528363943261764527906775893795625189651746165941438248136930298545695110631212696683271254403308539994170329875688236599305478130030194371971383054083049610267982461416568688720562725217837462387935392946474596966349477680685726377666929540130924122398746591270899232208239961618302848348129375606841006687727574503519146164506867574157671109933022528435615415554171024171300585408907077259610240139419075684581512703943171162496513070572546968852202777002845137863414028314025114932581655385254082418111977242759980115915504202336380850329162861826132885827910210346708045087589916666711356848614195462267049823085141386868421005551877773672329046391854000523197388175515628464457551891476514779819019668102328395639607489673081022505099
n = 204964538005458094391574690738766104196067587947267165575341074475716043971842449550067337731195102944823593489101699510575531541895593939634478254160200896755891641047742120885540191258962212405226135805491196590351987106011483652123110409148411537235255207358696047015199616340882291357173918540392964501976492251077110794432722042202109934588262870543755493029748475008610896164870659893013085704495216717998116109896882952474884270785733861739050889113464275228554841649603978281963688294995328883256317404081735364738985601286409677647577052211093127231530844271726386293348738817021732679704754961436390654856963930636538653822714234978179695778198536592408645222590877027896792957778186555118729335564281356291031440583078132397563914801937048297147819254611598144027963328749607393168101280779708669908245620694587176737529113823312930871616550632035759346759393976128246210013752530912953330415598837661326422094379798718827988692760848583517436061574821754507293943235476923624688378441177770313101393581916112910947153305055575974237171438666919114843946573283829704010962833299593770650238349021406868347635157566404829030358844616367849771415905381318344903398551946493709551783771889575282972265629264217620138873678733
enc = 58749077215207190492371298843854826665007067693641554277597021927783439106518176607848876784025881251057880587477892585242567469682290542409002363284991521084199535617805983767364935247518813883871587009725229910084882524866335007624383374126379502610933045897762967063766174922757656816300993939273687091280630401460905159739072179134897626330594985795970230333335492872721173603390854317323095769925904629970032658376378937924244589208035572848434030889091930182042226202356340798415809817722086119981262671540923062830870681500341640178082497128371291359953884993700348396920219975667972939044100089402796215197615549948516999318565775626034391795498234335228509335613253342179818268681240653806015040771731154600343889814141382273506238199460016081871283682838719833841393528105371834961952754168257271394981634141286257602629174903644009990944563870674888760807045240859970974837258567236802649772719645362361127488126570702845624169598462415354350277654287009645871674305081755840523910495569765451437265785385267255452210836618705384598344351666486694835670072372776263570462639412759703397195350879217144135006968472391258993407007505079063659488976186871280542665310586453539153772026697145449262179967269376262891840972187

root = iroot(n,4)[0]

p = root
assert isPrime(p)
q = root*root + (1<<256)
while not(isPrime(q)):
	q+=2

assert p*p*q == n

h = pow(g,n,n)
c = (enc*h)%n

# So to recover m we need to take the discrete logarithm with base g^(p-1)
b = pow(g,p-1,p*p) - 1
assert b%p == 0
b= b//p

a = pow(c,p-1,p*p) - 1
assert a%p == 0
a= a//p


b_ = invert(b,p)

m = (a*b_)%p
print(f"Flag: {long_to_bytes(m).decode()}")
