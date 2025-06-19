Presets: 

1. GET_EID
00a404000fa0000005591010ffffffff89000001:{7}
00c0000021 or ar
00e2910006bf3e035c015a
00c0000015 or ar

2. GET_PROFILE
00a404000fa0000005591010ffffffff89000001:{7}
00c0000021 or ar
00e2910003bf2d00
00c0000093 or ar

3. DISABLE_ESIM
00a404000fa0000005591010ffffffff89000001:{7}
00c0000021 or ar
00e2910014bf3211a00c5a0a{your iccid in little endian}810100
Example: 00e2910014bf3211a00c5a0a98010300002098509747810100
00c0000006 or ar

4. ENABLE_ESIM/SWITCH_ESIM
00a404000fa0000005591010ffffffff89000001:{7}
00c0000021 or ar
00e2910014bf3111a00c5a0a{your iccid in little endian}810100
Example: 00e2910014bf3111a00c5a0a98010300002098509747810100
00c0000006 or ar

5. DELETE_PROFILE
00a404000fa0000005591010ffffffff89000001:{7}
00c0000021 or ar
00e291000fbf330c5a0a{your iccid in little endian}
Example: 00e291000fbf330c5a0a98010300002098509747
00c0000006 or ar

6. PROFILE_DOWNLOAD
00a404000fa0000005591010ffffffff89000001:{7}
00c0000021 or ar
00e2910003bf2e00
00c0000015 or ar -> save to b64 as var1
00e2910003bf2000
00c0000038 or ar -> save to b64 as var2
run es9p_initiate_auth str:
TX:
{
	"smdpAddress":"consumer.e-sim.global",
	"euiccChallenge":var1,
	"euiccInfo1":var2
}
RX:
{
	"transactionId":var3,
	"serverSigned1":var4,
	"serverSignature1":var5,
	"euiccCiPKIdToBeUsed":var6,
	"serverCertificate":var7
}
00e2110x78{data}
data=b64ToHex(bf3882034a, var4, var5, var6, var7, matchingID)
00e29107070435290611a100
00c0000000 until SW1 SW2 is 61 xy
00c00000xy save all this as var8
run es9p_authenticate_client
TX:
url: {"smdpAddress"}/gsma/rsp2/es9plus/es9p_authenticate_client
{
	"transactionId" : var3,
	"authenticateServerResponse" : hexTob64(var8)
}
RX:
{
	"transactionId" : var3,
	"profileMetadata" : var9,
	"smdpSigned2" : var10,
	"smdpSignature2" : var11,
	"smdpCertificate" : var12
}
00e2110x78{data}
data=b64ToHex(bf218202d5, var10, var11, var12)
until SW1, SW2 = 61, xy
00c00000xy save this as var13
run es9p_get_bound_profile_package
TX:
url: {"smdpAddress"}/gsma/rsp2/es9plus/getBoundProfilePackage
{
	"transactionId" : var3,
	"prepareDownloadResponse" : hexTob64(var13)
}
RX:
{
	"transactionId" : var3,
	"boundProfilePackage" : var14
}
00e2110x78{data}
data=b64ToHex(var14 first 2 /s)
