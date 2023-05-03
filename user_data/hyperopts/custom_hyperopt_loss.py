# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Dict

from freqtrade.constants import Config
from freqtrade.optimize.hyperopt import IHyperOptLoss
from pandas import DataFrame


class CustomHyperOptLoss(IHyperOptLoss):
    @staticmethod
    def hyperopt_loss_function(
        results: DataFrame,
        trade_count: int,
        min_date: datetime,
        max_date: datetime,
        config: Config,
        processed: Dict[str, DataFrame],
        *args,
        **kwargs
    ) -> float:
        # 'pair', 'stake_amount', 'max_stake_amount', 'amount', 'open_date',
        # 'close_date', 'open_rate', 'close_rate', 'fee_open', 'fee_close',
        # 'trade_duration', 'profit_ratio', 'profit_abs', 'exit_reason',
        # 'initial_stop_loss_abs', 'initial_stop_loss_ratio', 'stop_loss_abs',
        # 'stop_loss_ratio', 'min_rate', 'max_rate', 'is_open', 'enter_tag',
        # 'leverage', 'is_short', 'open_timestamp', 'close_timestamp', 'orders'

        profit_ratio = results["profit_ratio"]
        trades = len(results)
        total_profit_abs = results["profit_abs"].sum()
        total_profit_ratio = profit_ratio.sum()
        # profitable_trades = trades - profit_ratio.lt(0).sum()
        profitable_trades = profit_ratio.gt(0).sum()
        percentage_trades_won = profitable_trades / trades * 100

        if trades < 10:
            return 0

        if total_profit_abs <= 0:
            return 0

        if total_profit_ratio <= 0:
            return 0

        if percentage_trades_won < 50:
            return 0

        # if percentage_trades_won == 100:
        #     return 0

        norm_factor = 0.8 + 0.2
        weighted = (
            (0.8 * percentage_trades_won / 100) + (0.2 * total_profit_abs / 100)
        ) / norm_factor

        return 0 - weighted


# 0.01% 	$1,015 	$4,243 	356 	EQIFi EQIFi / Tether Tether 	EQX/USDT
# 0.01% 	$1,117 	$1,177 	203 	Origin Dollar Governance Origin ... / Tether Tether 	OGV/USDT
# 0.01% 	$1,194,322 	$1,144,387 	1 	Bitcoin Bitcoin / Tether Tether 	BTC/USDT
# 0.01% 	$11,061 	$2,761 	370 	Yield App Yield App / Tether Tether 	YLD/USDT
# 0.01% 	$138,285 	$177,936 	30 	Ethereum Ethereum / USD Coin USD Coin 	ETH/USDC
# 0.01% 	$144,092 	$104,282 	7 	Ethereum Ethereum / Bitcoin Bitcoin 	ETH/BTC
# 0.01% 	$145,087 	$210,217 	27 	BNB BNB / Tether Tether 	BNB/USDT
# 0.01% 	$152,913 	$157,472 	23 	Cardano Cardano / Tether Tether 	ADA/USDT
# 0.01% 	$158,585 	$141,177 	52 	Binance USD Binance... / Tether Tether 	BUSD/USDT
# 0.01% 	$18,962 	$50,113 	223 	WOO Network WOO Net... / Tether Tether 	WOO/USDT
# 0.01% 	$2,162 	$5,675 	411 	Matrix AI Network Matrix ... / Tether Tether 	MAN/USDT
# 0.01% 	$2,296,988 	$618,795 	33 	USD Coin USD Coin / Tether Tether 	USDC/USDT
# 0.01% 	$22,761 	$54,505 	290 	BNB BNB / Bitcoin Bitcoin 	BNB/BTC
# 0.01% 	$327,436 	$326,972 	16 	Bitcoin Bitcoin / USD Coin USD Coin 	BTC/USDC
# 0.01% 	$444 	$9,661 	300 	Crypterium Crypterium / Tether Tether 	CRPT/USDT
# 0.01% 	$5,003 	$1,012 	464 	Exeedme Exeedme / Tether Tether 	XED/USDT
# 0.01% 	$5,244 	$3,760 	310 	Concordium Concordium / Tether Tether 	CCD/USDT
# 0.01% 	$54,518 	$84,362 	46 	NEAR Protocol NEAR Pr... / Tether Tether 	NEAR/USDT
# 0.01% 	$555,590 	$995,487 	4 	XRP XRP / Tether Tether 	XRP/USDT
# 0.01% 	$57,075 	$94,728 	25 	Mask Network Mask Ne... / Tether Tether 	MASK/USDT
# 0.01% 	$64,998 	$43,330 	106 	KuCoin KuCoin / Tether Tether 	KCS/USDT
# 0.01% 	$646,963 	$864,438 	2 	Ethereum Ethereum / Tether Tether 	ETH/USDT
# 0.01% 	$7,034 	$13,773 	311 	TRON TRON / USD Coin USD Coin 	TRX/USDC
# 0.01% 	$9,580 	$8,929 	700 	RMRK RMRK / Tether Tether 	RMRK/USDT
# 0.01% 	$966,343 	$824,872 	29 	Tether Tether / USD Coin USD Coin 	USDT/USDC
# 0.02% 	$1,155 	$4,849 	569 	PolkaBridge PolkaBr... / Tether Tether 	PBR/USDT
# 0.02% 	$1,941 	$8,855 	453 	Ergo Ergo / Tether Tether 	ERG/USDT
# 0.02% 	$10,965 	$24,971 	616 	Horizen Horizen / Tether Tether 	ZEN/USDT
# 0.02% 	$108,270 	$120,828 	60 	Stellar Stellar / Tether Tether 	XLM/USDT
# 0.02% 	$132,949 	$248,997 	357 	Tether Tether / TrueUSD TrueUSD 	USDT/TUSD
# 0.02% 	$174,925 	$242,820 	10 	Fantom Fantom / Tether Tether 	FTM/USDT
# 0.02% 	$2,594 	$6,325 	102 	Everscale Everscale / Tether Tether 	EVER/USDT
# 0.02% 	$210,735 	$304,745 	9 	Solana Solana / Tether Tether 	SOL/USDT
# 0.02% 	$22,350 	$14,980 	713 	Stellar Stellar / Ethereum Ethereum 	XLM/ETH
# 0.02% 	$221 	$333 	158 	X World Games X World... / Tether Tether 	XWG/USDT
# 0.02% 	$24,323 	$35,750 	265 	yearn.finance yearn.f... / Tether Tether 	YFI/USDT
# 0.02% 	$242,219 	$241,842 	24 	Shiba Inu Shiba Inu / Tether Tether 	SHIB/USDT
# 0.02% 	$255,250 	$262,128 	20 	Polygon Polygon / Tether Tether 	MATIC/USDT
# 0.02% 	$270,702 	$305,882 	13 	Arbitrum Arbitrum / Tether Tether 	ARB/USDT
# 0.02% 	$292 	$2,136 	365 	GAMEE GAMEE / Tether Tether 	GMEE/USDT
# 0.02% 	$3,228 	$6,079 	295 	Cream Cream / Tether Tether 	CREAM/USDT
# 0.02% 	$31,659 	$68,349 	86 	Quant Quant / Tether Tether 	QNT/USDT
# 0.02% 	$4,090 	$29,008 	730 	Polkadot Polkadot / USD Coin USD Coin 	DOT/USDC
# 0.02% 	$4,236 	$152 	469 	MARS4 MARS4 / Tether Tether 	MARS4/USDT
# 0.02% 	$580,750 	$663,248 	5 	Dogecoin Dogecoin / Tether Tether 	DOGE/USDT
# 0.02% 	$63,979 	$52,223 	32 	Terra Luna Classic Terra L... / Tether Tether 	LUNC/USDT
# 0.02% 	$757 	$502 	478 	Torum Torum / Tether Tether 	XTM/USDT
# 0.02% 	$79,985 	$280,011 	155 	Tether Tether / Dai Dai 	USDT/DAI
# 0.02% 	$8,486 	$9,243 	368 	BitTorrent BitTorrent / Tether Tether 	BTT/USDT
# 0.02% 	$80,542 	$118,527 	34 	TRON TRON / Tether Tether 	TRX/USDT
# 0.02% 	$844 	$2,925 	614 	Souni Souni / Tether Tether 	SON/USDT
# 0.03% 	$1,077 	$5,107 	61 	Creditcoin Creditcoin / Tether Tether 	CTC/USDT
# 0.03% 	$119,188 	$267,406 	15 	Litecoin Litecoin / Tether Tether 	LTC/USDT
# 0.03% 	$12,410 	$16,594 	574 	KuCoin KuCoin / Bitcoin Bitcoin 	KCS/BTC
# 0.03% 	$144,166 	$134,425 	35 	Avalanche Avalanche / Tether Tether 	AVAX/USDT
# 0.03% 	$15,895 	$14,390 	72 	Astra Protocol Astra P... / Tether Tether 	ASTRA/USDT
# 0.03% 	$19,195 	$22,447 	673 	Polygon Polygon / Bitcoin Bitcoin 	MATIC/BTC
# 0.03% 	$19,881 	$2,095 	226 	Push Protocol Push Pr... / Tether Tether 	PUSH/USDT
# 0.03% 	$2,156 	$332,640 	144 	DSLA Protocol DSLA Pr... / Tether Tether 	DSLA/USDT
# 0.03% 	$270 	$6,977 	702 	Wilder World Wilder ... / Tether Tether 	WILD/USDT
# 0.03% 	$29,510 	$61,313 	85 	THORChain THORChain / Tether Tether 	RUNE/USDT
# 0.03% 	$303 	$2,188 	189 	hiUNDEAD hiUNDEAD / Tether Tether 	HIUNDEAD/USDT
# 0.03% 	$43,355 	$56,448 	655 	Polkadot Polkadot / Bitcoin Bitcoin 	DOT/BTC
# 0.03% 	$44,929 	$72,493 	103 	Oasis Network Oasis N... / Tether Tether 	ROSE/USDT
# 0.03% 	$5,087 	$1,543 	611 	chrono.tech chrono.... / Tether Tether 	TIME/USDT
# 0.03% 	$571 	$34 	467 	Ndau Ndau / Tether Tether 	NDAU/USDT
# 0.03% 	$58,044 	$180,736 	353 	Binance USD Binance... / USD Coin USD Coin 	BUSD/USDC
# 0.03% 	$8,193 	$9,617 	383 	Telos Telos / Tether Tether 	TLOS/USDT
# 0.03% 	$90,322 	$185,695 	43 	Polkadot Polkadot / Tether Tether 	DOT/USDT
# 0.04% 	$1,699 	$5,810 	248 	Metaland Shares Metalan... / Tether Tether 	MLS/USDT
# 0.04% 	$102,525 	$131,070 	124 	XRP XRP / USD Coin USD Coin 	XRP/USDC
# 0.04% 	$12,435 	$15,901 	747 	BNB BNB / USD Coin USD Coin 	BNB/USDC
# 0.04% 	$13,071 	$41,243 	639 	TRON TRON / Bitcoin Bitcoin 	TRX/BTC
# 0.04% 	$2,013 	$14,616 	138 	MAP Protocol MAP Pro... / Tether Tether 	MAP/USDT
# 0.04% 	$2,038 	$2,311 	421 	Chain Guardians Chain G... / Tether Tether 	CGG/USDT
# 0.04% 	$2,333 	$5,477 	298 	FireStarter FireSta... / Tether Tether 	FLAME/USDT
# 0.04% 	$20,639 	$51,078 	73 	Kadena Kadena / Tether Tether 	KDA/USDT
# 0.04% 	$21,563 	$56,086 	11 	Terra Terra / Tether Tether 	LUNA/USDT
# 0.04% 	$28,318 	$14,386 	570 	USDD USDD / USD Coin USD Coin 	USDD/USDC
# 0.04% 	$3,972 	$6,786 	408 	Morpheus Labs Morpheu... / Tether Tether 	MITX/USDT
# 0.04% 	$4,680 	$3,334 	505 	Enzyme Enzyme / Tether Tether 	MLN/USDT
# 0.04% 	$451 	$677 	110 	Acquire.Fi Acquire.Fi / Tether Tether 	ACQ/USDT
# 0.04% 	$48,876 	$64,605 	96 	Waves Waves / Tether Tether 	WAVES/USDT
# 0.04% 	$5,850 	$19,423 	322 	Adventure Gold Adventu... / Tether Tether 	AGLD/USDT
# 0.04% 	$56,917 	$70,018 	90 	Maker Maker / Tether Tether 	MKR/USDT
# 0.04% 	$60,808 	$50,273 	242 	Cronos Cronos / Tether Tether 	CRO/USDT
# 0.04% 	$655 	$4,128 	142 	TitanSwap TitanSwap / Tether Tether 	TITAN/USDT
# 0.04% 	$74,143 	$100,113 	49 	Lido DAO Lido DAO / Tether Tether 	LDO/USDT
# 0.05% 	$1,955 	$8,819 	132 	BurgerCities BurgerC... / Tether Tether 	BURGER/USDT
# 0.05% 	$11,243 	$13,526 	625 	Cosmos Hub Cosmos Hub / Bitcoin Bitcoin 	ATOM/BTC
# 0.05% 	$13,800 	$22,961 	369 	PancakeSwap Pancake... / Tether Tether 	CAKE/USDT
# 0.05% 	$132,630 	$163,740 	55 	Algorand Algorand / Tether Tether 	ALGO/USDT
# 0.05% 	$14,943 	$18,360 	192 	TerraClassicUSD TerraCl... / Tether Tether 	USTC/USDT
# 0.05% 	$177,907 	$288,363 	44 	Aptos Aptos / Tether Tether 	APT/USDT
# 0.05% 	$19,318 	$28,298 	289 	Polygon Polygon / USD Coin USD Coin 	MATIC/USDC
# 0.05% 	$2,886 	$6,400 	305 	Uno Re Uno Re / Tether Tether 	UNO/USDT
# 0.05% 	$21,720 	$42,823 	234 	GMX GMX / Tether Tether 	GMX/USDT
# 0.05% 	$223 	$324 	419 	Polychain Monsters Polycha... / Tether Tether 	PMON/USDT
# 0.05% 	$28,302 	$42,526 	200 	SPACE ID SPACE ID / Tether Tether 	ID/USDT
# 0.05% 	$43,132 	$82,312 	98 	Theta Network Theta N... / Tether Tether 	THETA/USDT
# 0.05% 	$43,425 	$105,097 	149 	STEPN STEPN / Tether Tether 	GMT/USDT
# 0.05% 	$44,518 	$27,036 	38 	Velo Velo / Tether Tether 	VELO/USDT
# 0.05% 	$5,329 	$3,813 	133 	Aurigami Aurigami / Tether Tether 	PLY/USDT
# 0.05% 	$54,125 	$86,345 	97 	ApeCoin ApeCoin / Tether Tether 	APE/USDT
# 0.05% 	$54,571 	$179,557 	57 	Cosmos Hub Cosmos Hub / Tether Tether 	ATOM/USDT
# 0.05% 	$565 	$625 	578 	Metaverse.Network Pioneer Metaver... / Tether Tether 	NEER/USDT
# 0.05% 	$57,385 	$110,362 	50 	Chainlink Chainlink / Tether Tether 	LINK/USDT
# 0.05% 	$59,110 	$67,169 	95 	Decentraland Decentr... / Tether Tether 	MANA/USDT
# 0.05% 	$7,018 	$27,441 	606 	Storj Storj / Tether Tether 	STORJ/USDT
# 0.05% 	$7,864 	$18,845 	620 	Theta Fuel Theta Fuel / Tether Tether 	TFUEL/USDT
# 0.06% 	$133,585 	$106,647 	62 	Hedera Hedera / Tether Tether 	HBAR/USDT
# 0.06% 	$14,934 	$10,637 	22 	Verasity Verasity / Tether Tether 	VRA/USDT
# 0.06% 	$142,879 	$227,400 	12 	Monero Monero / Tether Tether 	XMR/USDT
# 0.06% 	$2,231 	$1,132 	147 	UpOnly UpOnly / Tether Tether 	UPO/USDT
# 0.06% 	$2,956 	$51,145 	647 	Litecoin Litecoin / Ethereum Ethereum 	LTC/ETH
# 0.06% 	$209 	$492 	550 	Lovelace World Lovelac... / Tether Tether 	LACE/USDT
# 0.06% 	$230,725 	$146,133 	17 	Conflux Conflux / Tether Tether 	CFX/USDT
# 0.06% 	$25,629 	$65,404 	180 	Axie Infinity Axie In... / Tether Tether 	AXS/USDT
# 0.06% 	$29,501 	$83,796 	71 	Render Render / Tether Tether 	RNDR/USDT
# 0.06% 	$34,528 	$37,460 	236 	Ankr Network Ankr Ne... / Tether Tether 	ANKR/USDT
# 0.06% 	$36,166 	$65,733 	208 	Uniswap Uniswap / Tether Tether 	UNI/USDT
# 0.06% 	$428 	$471 	745 	Plutonian DAO Plutoni... / Tether Tether 	PLD/USDT
# 0.06% 	$45,122 	$45,246 	213 	Tezos Tezos / Tether Tether 	XTZ/USDT
# 0.06% 	$47,713 	$111,163 	307 	Bitcoin Cash Bitcoin... / Tether Tether 	BCH/USDT
# 0.06% 	$534 	$2,348 	204 	TemDAO TemDAO / Tether Tether 	TEM/USDT
# 0.06% 	$54,939 	$69,410 	79 	The Sandbox The San... / Tether Tether 	SAND/USDT
# 0.06% 	$58,387 	$104,436 	41 	Filecoin Filecoin / Tether Tether 	FIL/USDT
# 0.06% 	$6,519 	$3,055 	66 	hiBAYC hiBAYC / Tether Tether 	HIBAYC/USDT
# 0.06% 	$7,217 	$21,446 	281 	DUSK Network DUSK Ne... / Tether Tether 	DUSK/USDT
# 0.06% 	$729 	$3,584 	174 	hiODBS hiODBS / Tether Tether 	HIODBS/USDT
# 0.06% 	$74,974 	$115,364 	78 	dYdX dYdX / Tether Tether 	DYDX/USDT
# 0.06% 	$767 	$2,767 	471 	BNS BNS / Tether Tether 	BNS/USDT
# 0.06% 	$9,465 	$25,073 	465 	USDD USDD / Tether Tether 	USDD/USDT
# 0.06% 	$91,910 	$75,954 	690 	Celo Dollar Celo Do... / Tether Tether 	CUSD/USDT
# 0.07% 	$10,106 	$6,434 	609 	Alkimi Alkimi / Tether Tether 	$ADS/USDT
# 0.07% 	$10,334 	$12,900 	81 	Proton Proton / Tether Tether 	XPR/USDT
# 0.07% 	$11,092 	$10,961 	136 	Klever Klever / Tether Tether 	KLV/USDT
# 0.07% 	$12,273 	$60,762 	82 	Enjin Coin Enjin Coin / Tether Tether 	ENJ/USDT
# 0.07% 	$12,771 	$26,655 	373 	Aragon Aragon / Tether Tether 	ANT/USDT
# 0.07% 	$14,876 	$38,684 	125 	Arweave Arweave / Tether Tether 	AR/USDT
# 0.07% 	$19,823 	$31,562 	3 	Toncoin Toncoin / Tether Tether 	TON/USDT
# 0.07% 	$24,369 	$74,483 	264 	Cardano Cardano / Bitcoin Bitcoin 	ADA/BTC
# 0.07% 	$24,584 	$36,533 	355 	Cardano Cardano / USD Coin USD Coin 	ADA/USDC
# 0.07% 	$251 	$287 	247 	MoonStarter MoonSta... / Tether Tether 	MNST/USDT
# 0.07% 	$32,833 	$47,630 	135 	Dash Dash / Tether Tether 	DASH/USDT
# 0.07% 	$35,956 	$46,672 	40 	Chiliz Chiliz / Tether Tether 	CHZ/USDT
# 0.07% 	$36,469 	$34,352 	228 	XDC Network XDC Net... / Tether Tether 	XDC/USDT
# 0.07% 	$5,351 	$12,675 	332 	Orion Protocol Orion P... / Tether Tether 	ORN/USDT
# 0.07% 	$52,559 	$69,560 	241 	Dogecoin Dogecoin / Bitcoin Bitcoin 	DOGE/BTC
# 0.07% 	$635 	$11,935 	321 	CareCoin CareCoin / Tether Tether 	CARE/USDT
# 0.07% 	$65,377 	$144,965 	18 	SingularityNET Singula... / Tether Tether 	AGIX/USDT
# 0.07% 	$653 	$872 	159 	hiENS4 hiENS4 / Tether Tether 	HIENS4/USDT
# 0.07% 	$7,894 	$28,400 	458 	Shiba Inu Shiba Inu / USD Coin USD Coin 	SHIB/USDC
# 0.07% 	$955 	$4,346 	179 	hiMOONBIRDS hiMOONB... / Tether Tether 	HIMOONBIRD...
# 0.08% 	$118,370 	$124,008 	19 	Stacks Stacks / Tether Tether 	STX/USDT
# 0.08% 	$12,717 	$44,756 	109 	Frax Share Frax Share / Tether Tether 	FXS/USDT
# 0.08% 	$15,660 	$44,678 	131 	Ocean Protocol Ocean P... / Tether Tether 	OCEAN/USDT
# 0.08% 	$2,775 	$12,952 	622 	Fantom Fantom / Ethereum Ethereum 	FTM/ETH
# 0.08% 	$2,961 	$28,109 	462 	Unizen Unizen / Tether Tether 	ZCX/USDT
# 0.08% 	$22,365 	$52,199 	42 	Zcash Zcash / Tether Tether 	ZEC/USDT
# 0.08% 	$24,813 	$17,215 	519 	Litecoin Litecoin / USD Coin USD Coin 	LTC/USDC
# 0.08% 	$30,269 	$67,793 	67 	VeChain VeChain / Tether Tether 	VET/USDT
# 0.08% 	$32,454 	$54,823 	122 	Ethereum Classic Ethereu... / Tether Tether 	ETC/USDT
# 0.08% 	$35,164 	$72,035 	532 	1inch 1inch / Tether Tether 	1INCH/USDT
# 0.08% 	$37,517 	$43,606 	14 	Alchemy Pay Alchemy... / Tether Tether 	ACH/USDT
# 0.08% 	$478 	$1,764 	439 	Meta Apes PEEL Meta Ap... / Tether Tether 	PEEL/USDT
# 0.08% 	$51,895 	$129,597 	69 	EOS EOS / Tether Tether 	EOS/USDT
# 0.08% 	$58,386 	$25,938 	572 	Stellar Stellar / Bitcoin Bitcoin 	XLM/BTC
# 0.08% 	$81,326 	$175,732 	74 	The Graph The Graph / Tether Tether 	GRT/USDT
# 0.08% 	$9,857 	$18,469 	319 	Bloktopia Bloktopia / Tether Tether 	BLOK/USDT
# 0.08% 	$9,945 	$12,354 	459 	Chainlink Chainlink / USD Coin USD Coin 	LINK/USDC
# 0.09% 	$1,010 	$4,240 	47 	HALOnft.art HALOnft... / Tether Tether 	HALO/USDT
# 0.09% 	$1,110 	$2,882 	166 	DeRace DeRace / Tether Tether 	DERC/USDT
# 0.09% 	$10,701 	$9,455 	303 	Moonriver Moonriver / Tether Tether 	MOVR/USDT
# 0.09% 	$10,891 	$31,137 	328 	Dogelon Mars Dogelon... / Tether Tether 	ELON/USDT
# 0.09% 	$123,398 	$133,945 	75 	Blur Blur / Tether Tether 	BLUR/USDT
# 0.09% 	$126,305 	$129,942 	26 	Monero Monero / Bitcoin Bitcoin 	XMR/BTC
# 0.09% 	$16,666 	$25,107 	537 	Band Protocol Band Pr... / Tether Tether 	BAND/USDT
# 0.09% 	$17,752 	$10,916 	182 	Energy Web Energy Web / Tether Tether 	EWT/USDT
# 0.09% 	$183,358 	$167,737 	45 	Optimism Optimism / Tether Tether 	OP/USDT
# 0.09% 	$190 	$2,486 	610 	Kingdomverse Kingdom... / Tether Tether 	KING/USDT
# 0.09% 	$2,505 	$2,279 	296 	Woonkly Power Woonkly... / Tether Tether 	WOOP/USDT
# 0.09% 	$2,570 	$9,656 	688 	Akropolis Akropolis / Tether Tether 	AKRO/USDT
# 0.09% 	$2,992 	$2,525 	65 	Polylastic Polylastic / Tether Tether 	POLX/USDT
# 0.09% 	$24,190 	$65,951 	161 	PAX Gold PAX Gold / Tether Tether 	PAXG/USDT
# 0.09% 	$24,233 	$40,452 	442 	Kusama Kusama / Tether Tether 	KSM/USDT
# 0.09% 	$27,004 	$72,115 	283 	Litecoin Litecoin / Bitcoin Bitcoin 	LTC/BTC
# 0.09% 	$3,145 	$4,103 	725 	Orbs Orbs / Tether Tether 	ORBS/USDT
# 0.09% 	$3,204 	$4,902 	429 	OpenDAO OpenDAO / Tether Tether 	SOS/USDT
# 0.09% 	$3,884 	$10,938 	299 	Clover Finance Clover ... / Tether Tether 	CLV/USDT
# 0.09% 	$4,743 	$2,830 	597 	MojitoSwap MojitoSwap / Tether Tether 	MJT/USDT
# 0.09% 	$41,198 	$56,535 	187 	Magic Magic / Tether Tether 	MAGIC/USDT
# 0.09% 	$540 	$1,752 	461 	Revuto Revuto / Tether Tether 	REVU/USDT
# 0.09% 	$56,865 	$93,130 	156 	Curve DAO Curve DAO / Tether Tether 	CRV/USDT
# 0.09% 	$6,372 	$6,665 	497 	XYO Network XYO Net... / Tether Tether 	XYO/USDT
# 0.09% 	$7,628 	$13,211 	585 	Avalanche Avalanche / USD Coin USD Coin 	AVAX/USDC
# 0.09% 	$767 	$1,080 	327 	Effect Network Effect ... / Tether Tether 	EFX/USDT
# 0.09% 	$775 	$2,576 	251 	hiOD hiOD / Tether Tether 	HIOD/USDT
# 0.09% 	$80,345 	$100,047 	8 	JasmyCoin JasmyCoin / Tether Tether 	JASMY/USDT
# 0.09% 	$9,790 	$12,730 	689 	Cosmos Hub Cosmos Hub / USD Coin USD Coin 	ATOM/USDC
# 0.1% 	$107,217 	$128,280 	77 	GALA GALA / Tether Tether 	GALA/USDT
# 0.1% 	$108,652 	$123,002 	31 	SXP SXP / Tether Tether 	SXP/USDT
# 0.1% 	$13,583 	$10,759 	388 	Travala.com Travala... / Tether Tether 	AVA/USDT
# 0.1% 	$22,928 	$23,852 	341 	Solana Solana / USD Coin USD Coin 	SOL/USDC
# 0.1% 	$25,811 	$100,889 	233 	MultiversX MultiversX / Tether Tether 	EGLD/USDT
# 0.1% 	$3,803 	$10,124 	694 	Dash Dash / Bitcoin Bitcoin 	DASH/BTC
# 0.1% 	$32,792 	$56,063 	91 	Harmony Harmony / Tether Tether 	ONE/USDT
# 0.1% 	$35,062 	$69,694 	134 	ImmutableX ImmutableX / Tether Tether 	IMX/USDT
# 0.1% 	$37,831 	$53,827 	164 	Aave Aave / Tether Tether 	AAVE/USDT
# 0.1% 	$4,334 	$16,679 	351 	Chia Chia / Tether Tether 	XCH/USDT
# 0.1% 	$457 	$529 	190 	Starly Starly / Tether Tether 	STARLY/USDT
# 0.1% 	$49,991 	$96,699 	205 	Zilliqa Zilliqa / Tether Tether 	ZIL/USDT
# 0.1% 	$5,449 	$14,714 	117 	Router Protocol Router ... / Tether Tether 	ROUTE/USDT
# 0.1% 	$874 	$1,767 	529 	Alchemy Alchemy / Tether Tether 	ACOIN/USDT
# 0.11% 	$1,444 	$7,192 	685 	Haven Haven / Tether Tether 	XHV/USDT
# 0.11% 	$1,919 	$580 	301 	IguVerse IGU IguVers... / Tether Tether 	IGU/USDT
# 0.11% 	$11,250 	$16,918 	520 	Tellor Tributes Tellor ... / Tether Tether 	TRB/USDT
# 0.11% 	$14,217 	$30,399 	93 	FLOKI FLOKI / Tether Tether 	FLOKI/USDT
# 0.11% 	$15,231 	$16,525 	201 	Yield Guild Games Yield G... / Tether Tether 	YGG/USDT
# 0.11% 	$17,279 	$22,596 	583 	Livepeer Livepeer / Tether Tether 	LPT/USDT
# 0.11% 	$3,432 	$1,371 	304 	Ispolink Ispolink / Tether Tether 	ISP/USDT
# 0.11% 	$3,499 	$15,979 	336 	JUST JUST / Tether Tether 	JST/USDT
# 0.11% 	$35,540 	$52,554 	100 	Celo Celo / Tether Tether 	CELO/USDT
# 0.11% 	$36,859 	$53,759 	146 	Synthetix Network Synthet... / Tether Tether 	SNX/USDT
# 0.11% 	$4,736 	$7,140 	698 	CEEK Smart VR CEEK Sm... / Tether Tether 	CEEK/USDT
# 0.11% 	$42 	$478 	196 	hiVALHALLA hiVALHALLA / Tether Tether 	HIVALHALLA...
# 0.11% 	$45,084 	$55,203 	225 	Dogecoin Dogecoin / USD Coin USD Coin 	DOGE/USDC
# 0.11% 	$5,507 	$9,815 	460 	MANTRA MANTRA / Tether Tether 	OM/USDT
# 0.11% 	$5,611 	$5,025 	699 	TRVL TRVL / Bitcoin Bitcoin 	TRVL/BTC
# 0.11% 	$52,128 	$72,196 	445 	Loopring Loopring / Tether Tether 	LRC/USDT
# 0.11% 	$55,778 	$67,558 	99 	NEO NEO / Tether Tether 	NEO/USDT
# 0.11% 	$58,989 	$139,407 	230 	XRP XRP / Bitcoin Bitcoin 	XRP/BTC
# 0.11% 	$6,126 	$70,765 	538 	Fetch.ai Fetch.ai / Bitcoin Bitcoin 	FET/BTC
# 0.11% 	$675 	$925 	162 	hiSQUIGGLE hiSQUIGGLE / Tether Tether 	HISQUIGGLE...
# 0.11% 	$9,104 	$8,625 	541 	Komodo Komodo / Tether Tether 	KMD/USDT
# 0.11% 	$9,682 	$23,377 	215 	Basic Attention Basic A... / Tether Tether 	BAT/USDT
# 0.12% 	$10,300 	$22,786 	207 	ICON ICON / Tether Tether 	ICX/USDT
# 0.12% 	$120,119 	$206,538 	119 	Fetch.ai Fetch.ai / Tether Tether 	FET/USDT
# 0.12% 	$14,560 	$36,515 	151 	Reserve Rights Reserve... / Tether Tether 	RSR/USDT
# 0.12% 	$15,159 	$21,433 	219 	My Neighbor Alice My Neig... / Tether Tether 	ALICE/USDT
# 0.12% 	$16,326 	$33,329 	64 	Radix Radix / Tether Tether 	XRD/USDT
# 0.12% 	$16,633 	$41,481 	582 	Ethereum Name Service Ethereu... / Tether Tether 	ENS/USDT
# 0.12% 	$2,305 	$1,020 	163 	PIAS PIAS / Tether Tether 	PIAS/USDT
# 0.12% 	$3,066 	$902 	433 	ThunderCore Thunder... / Tether Tether 	TT/USDT
# 0.12% 	$3,806 	$10,122 	224 	League of Kingdoms League ... / Tether Tether 	LOKA/USDT
# 0.12% 	$36,186 	$49,951 	87 	Sushi Sushi / Tether Tether 	SUSHI/USDT
# 0.12% 	$37,396 	$25,703 	493 	REN REN / Tether Tether 	REN/USDT
# 0.12% 	$4,589 	$20,021 	657 	Fantom Fantom / Bitcoin Bitcoin 	FTM/BTC
# 0.12% 	$4,636 	$7,449 	153 	SHILL Token SHILL T... / Tether Tether 	SHILL/USDT
# 0.12% 	$5,074 	$10,888 	366 	Metal DAO Metal DAO / Tether Tether 	MTL/USDT
# 0.12% 	$5,158 	$21,937 	126 	Access Protocol Access ... / Tether Tether 	ACS/USDT
# 0.12% 	$6,337 	$21,063 	748 	Ravencoin Ravencoin / Tether Tether 	RVN/USDT
# 0.12% 	$7,543 	$23,416 	194 	Compound Compound / Tether Tether 	COMP/USDT
# 0.12% 	$8,155 	$29,176 	420 	Mina Protocol Mina Pr... / Tether Tether 	MINA/USDT
# 0.12% 	$8,283 	$6,893 	210 	KOK KOK / Tether Tether 	KOK/USDT
# 0.12% 	$8,634 	$13,271 	707 	Nano Nano / Tether Tether 	XNO/USDT
# 0.13% 	$1,000 	$10,063 	592 	Synapse Synapse / Tether Tether 	SYN/USDT
# 0.13% 	$10,148 	$13,013 	591 	Fantom Fantom / USD Coin USD Coin 	FTM/USDC
# 0.13% 	$12,037 	$38,166 	526 	API3 API3 / Tether Tether 	API3/USDT
# 0.13% 	$16,330 	$37,671 	160 	Audius Audius / Tether Tether 	AUDIO/USDT
# 0.13% 	$20,839 	$25,669 	21 	Smooth Love Potion Smooth ... / Tether Tether 	SLP/USDT
# 0.13% 	$21,414 	$11,831 	278 	COTI COTI / Tether Tether 	COTI/USDT
# 0.13% 	$22,584 	$20,790 	670 	IOST IOST / Tether Tether 	IOST/USDT
# 0.13% 	$3,204 	$28,424 	287 	Phala Phala / Tether Tether 	PHA/USDT
# 0.13% 	$3,246 	$33,112 	231 	Moonbeam Moonbeam / Tether Tether 	GLMR/USDT
# 0.13% 	$4,848 	$4,008 	489 	Gods Unchained Gods Un... / Tether Tether 	GODS/USDT
# 0.13% 	$48,399 	$38,350 	108 	Tribal Token Tribal ... / Tether Tether 	TRIBL/USDT
# 0.13% 	$5,599 	$15,691 	624 	Algorand Algorand / Bitcoin Bitcoin 	ALGO/BTC
# 0.13% 	$5,945 	$3,646 	252 	APENFT APENFT / Tether Tether 	NFT/USDT
# 0.13% 	$9,550 	$4,891 	107 	PRIMAL PRIMAL / Tether Tether 	PRIMAL/USDT
# 0.14% 	$12,768 	$20,079 	446 	EthereumPoW Ethereu... / Tether Tether 	ETHW/USDT
# 0.14% 	$16,818 	$99,850 	104 	Vulcan Forged Vulcan ... / Tether Tether 	PYR/USDT
# 0.14% 	$18,136 	$31,501 	531 	OMG Network OMG Net... / Tether Tether 	OMG/USDT
# 0.14% 	$2,110 	$10,920 	661 	Reef Reef / Tether Tether 	REEF/USDT
# 0.14% 	$2,595 	$1,242 	617 	Gemie Gemie / Tether Tether 	GEM/USDT
# 0.14% 	$22,459 	$32,786 	185 	Astar Astar / Tether Tether 	ASTR/USDT
# 0.14% 	$23,997 	$29,037 	490 	IoTeX IoTeX / Tether Tether 	IOTX/USDT
# 0.14% 	$24,442 	$40,658 	426 	SKALE SKALE / Tether Tether 	SKL/USDT
# 0.14% 	$28,844 	$23,197 	92 	Nervos Network Nervos ... / Tether Tether 	CKB/USDT
# 0.14% 	$28,878 	$117,713 	375 	Kava Kava / Tether Tether 	KAVA/USDT
# 0.14% 	$43,862 	$79,556 	48 	Monero Monero / Ethereum Ethereum 	XMR/ETH
# 0.14% 	$6,659 	$6,783 	268 	The Virtua Kolect The Vir... / Tether Tether 	TVK/USDT
# 0.14% 	$7,428 	$16,098 	667 	ApeCoin ApeCoin / USD Coin USD Coin 	APE/USDC
# 0.14% 	$8,712 	$8,376 	653 	Cosmos Hub Cosmos Hub / Ethereum Ethereum 	ATOM/ETH
# 0.14% 	$85,839 	$146,809 	28 	Injective Injective / Tether Tether 	INJ/USDT
# 0.14% 	$9,311 	$21,482 	662 	TRON TRON / Ethereum Ethereum 	TRX/ETH
# 0.15% 	$109,767 	$62,769 	503 	Tether (USDT) Tether 	USDT/EUR
# 0.15% 	$13,940 	$19,004 	398 	DigiByte DigiByte / Tether Tether 	DGB/USDT
# 0.15% 	$2,572 	$1,161 	547 	OpenLeverage OpenLev... / Tether Tether 	OLE/USDT
# 0.15% 	$22,440 	$29,110 	262 	Coin98 Coin98 / Tether Tether 	C98/USDT
# 0.15% 	$27,640 	$7,899 	564 	Klever Klever / Bitcoin Bitcoin 	KLV/BTC
# 0.15% 	$280 	$4,530 	313 	Divi Divi / Tether Tether 	DIVI/USDT
# 0.15% 	$4,724 	$22,523 	623 	NEAR Protocol NEAR Pr... / USD Coin USD Coin 	NEAR/USDC
# 0.15% 	$4,883 	$7,404 	517 	MovieBloc MovieBloc / Tether Tether 	MBL/USDT
# 0.15% 	$50,164 	$58,304 	129 	Hashflow Hashflow / Tether Tether 	HFT/USDT
# 0.15% 	$552 	$958 	237 	Acent Acent / Tether Tether 	ACE/USDT
# 0.15% 	$596 	$4,896 	560 	TribeOne TribeOne / Tether Tether 	HAKA/USDT
# 0.15% 	$639 	$290 	277 	Kava Swap Kava Swap / Tether Tether 	SWP/USDT
# 0.16% 	$1,160 	$11,011 	363 	Presearch Presearch / Tether Tether 	PRE/USDT
# 0.16% 	$10,419 	$13,015 	239 	Beldex Beldex / Tether Tether 	BDX/USDT
# 0.16% 	$12,360 	$16,847 	634 	KuCoin KuCoin / Ethereum Ethereum 	KCS/ETH
# 0.16% 	$16,139 	$60,380 	39 	Linear Linear / Tether Tether 	LINA/USDT
# 0.16% 	$2,142 	$2,428 	566 	Wombat Wombat / Tether Tether 	WOMBAT/USDT
# 0.16% 	$2,675 	$11,238 	513 	Biswap Biswap / Tether Tether 	BSW/USDT
# 0.16% 	$2,760 	$10,501 	651 	Gains Network Gains N... / Tether Tether 	GNS/USDT
# 0.16% 	$2,792 	$584 	393 	Oddz Oddz / Tether Tether 	ODDZ/USDT
# 0.16% 	$20,681 	$34,249 	378 	ConstitutionDAO Constit... / Tether Tether 	PEOPLE/USDT
# 0.16% 	$22,842 	$30,792 	424 	Stacks Stacks / Bitcoin Bitcoin 	STX/BTC
# 0.16% 	$23,379 	$51,549 	596 	Bitcoin Bitcoin / TrueUSD TrueUSD 	BTC/TUSD
# 0.16% 	$3,912 	$2,819 	83 	Myria Myria / Tether Tether 	MYRIA/USDT
# 0.16% 	$48,493 	$22,868 	260 	Bitcoin Bitcoin / Dai Dai 	BTC/DAI
# 0.16% 	$5,195 	$14,283 	354 	Ambire AdEx Ambire ... / Tether Tether 	ADX/USDT
# 0.16% 	$7,762 	$13,420 	750 	Automata Automata / Tether Tether 	ATA/USDT
# 0.16% 	$708 	$7,537 	238 	Solanium Solanium / Tether Tether 	SLIM/USDT
# 0.17% 	$1,067 	$383 	76 	Superpower Squad Superpo... / Tether Tether 	SQUAD/USDT
# 0.17% 	$1,396 	$5,823 	280 	Kambria Kambria / Tether Tether 	KAT/USDT
# 0.17% 	$16,424 	$27,630 	379 	Klaytn Klaytn / Tether Tether 	KLAY/USDT
# 0.17% 	$18,969 	$25,895 	320 	COCOS BCX COCOS BCX / Tether Tether 	COCOS/USDT
# 0.17% 	$19,428 	$41,171 	576 	Chromia Chromia / Tether Tether 	CHR/USDT
# 0.17% 	$2,190 	$2,799 	677 	Nimiq Nimiq / Tether Tether 	NIM/USDT
# 0.17% 	$2,379 	$11,712 	410 	Ampleforth Governance Amplefo... / Tether Tether 	FORTH/USDT
# 0.17% 	$6,879 	$11,280 	581 	Mines of Dalarnia Mines o... / Tether Tether 	DAR/USDT
# 0.17% 	$633 	$6,257 	631 	Epik Prime Epik Prime / Tether Tether 	EPIK/USDT
# 0.17% 	$67,990 	$41,561 	285 	World Mobile Token World M... / Tether Tether 	WMT/USDT
# 0.17% 	$673 	$5,012 	742 	Qtum Qtum / Bitcoin Bitcoin 	QTUM/BTC
# 0.17% 	$9,285 	$1,832 	169 	hiDOODLES hiDOODLES / Tether Tether 	HIDOODLES/...
# 0.18% 	$1,156 	$2,158 	552 	IX Swap IX Swap / Tether Tether 	IXS/USDT
# 0.18% 	$1,796 	$6,417 	318 	Cirus Cirus / Tether Tether 	CIRUS/USDT
# 0.18% 	$10,121 	$15,591 	250 	SuperVerse SuperVerse / Tether Tether 	SUPER/USDT
# 0.18% 	$11,867 	$15,889 	679 	Request Request / Tether Tether 	REQ/USDT
# 0.18% 	$13,866 	$24,125 	437 	Origin Protocol Origin ... / Tether Tether 	OGN/USDT
# 0.18% 	$17,933 	$21,099 	121 	NKN NKN / Tether Tether 	NKN/USDT
# 0.18% 	$2,553 	$4,112 	415 	Tokoin Tokoin / Tether Tether 	TOKO/USDT
# 0.18% 	$28,779 	$45,638 	267 	Radiant Capital Radiant... / Tether Tether 	RDNT/USDT
# 0.18% 	$29,302 	$35,537 	409 	Liquity Liquity / Tether Tether 	LQTY/USDT
# 0.18% 	$35,527 	$55,928 	540 	XRP XRP / Ethereum Ethereum 	XRP/ETH
# 0.18% 	$373 	$734 	338 	SWFTCOIN SWFTCOIN / Tether Tether 	SWFTC/USDT
# 0.18% 	$6,167 	$9,031 	744 	Orchid Protocol Orchid ... / Tether Tether 	OXT/USDT
# 0.18% 	$6,401 	$33,388 	468 	IOTA IOTA / Tether Tether 	MIOTA/USDT
# 0.18% 	$7,074 	$24,389 	743 	Terra Luna Classic Terra L... / USD Coin USD Coin 	LUNC/USDC
# 0.18% 	$860 	$5,413 	551 	V.SYSTEMS V.SYSTEMS / Bitcoin Bitcoin 	VSYS/BTC
# 0.18% 	$9,502 	$24,787 	157 	Trust Wallet Trust W... / Tether Tether 	TWT/USDT
# 0.19% 	$1,039 	$4,007 	502 	Genshiro Genshiro / Tether Tether 	GENS/USDT
# 0.19% 	$1,103 	$355 	577 	LaunchBlock LaunchB... / Tether Tether 	LBP/USDT
# 0.19% 	$10,059 	$7,583 	229 	WEMIX WEMIX / Tether Tether 	WEMIX/USDT
# 0.19% 	$10,244 	$22,666 	249 	Bitgert Bitgert / Tether Tether 	BRISE/USDT
# 0.19% 	$10,923 	$9,843 	613 	Amp Amp / Tether Tether 	AMP/USDT
# 0.19% 	$12,970 	$32,763 	325 	Flow Flow / Tether Tether 	FLOW/USDT
# 0.19% 	$13,505 	$69,066 	143 	Flux Flux / Tether Tether 	FLUX/USDT
# 0.19% 	$15,129 	$12,212 	512 	Alien Worlds Alien W... / Tether Tether 	TLM/USDT
# 0.19% 	$15,632 	$29,719 	553 	Kyber Network Crystal Kyber N... / Tether Tether 	KNC/USDT
# 0.19% 	$2,303 	$1,681 	601 	Polkamarkets Polkama... / Tether Tether 	POLK/USDT
# 0.19% 	$2,913 	$10,480 	656 	UMA UMA / Tether Tether 	UMA/USDT
# 0.19% 	$356 	$933 	183 	hiCLONEX hiCLONEX / Tether Tether 	HICLONEX/USDT
# 0.19% 	$4,193 	$12,303 	701 	KardiaChain KardiaC... / Tether Tether 	KAI/USDT
# 0.19% 	$839 	$160 	697 	dotmoovs dotmoovs / Tether Tether 	MOOV/USDT
# 0.2% 	$1,189 	$362 	171 	hiFRIENDS hiFRIENDS / Tether Tether 	HIFRIENDS/...
# 0.2% 	$14,890 	$24,328 	425 	Litentry Litentry / Tether Tether 	LIT/USDT
# 0.2% 	$15,263 	$23,299 	70 	Unifi Protocol DAO Unifi P... / Tether Tether 	UNFI/USDT
# 0.2% 	$190 	$2,389 	603 	GameFi GameFi / Tether Tether 	GAFI/USDT
# 0.2% 	$2,267 	$7,149 	56 	Fracton Protocol Fracton... / Tether Tether 	FT/USDT
# 0.2% 	$3,372 	$20,493 	350 	Stargate Finance Stargat... / Tether Tether 	STG/USDT
# 0.2% 	$3,479 	$4,153 	367 	AirDAO AirDAO / Tether Tether 	AMB/USDT
# 0.2% 	$4,617 	$1,215 	116 	hiENS3 hiENS3 / Tether Tether 	HIENS3/USDT
# 0.2% 	$4,993 	$6,614 	36 	Alpine F1 Team Fan Token Alpine ... / Tether Tether 	ALPINE/USDT
# 0.2% 	$49,800 	$89,788 	89 	Internet Computer Interne... / Tether Tether 	ICP/USDT
# 0.2% 	$508 	$1,453 	172 	hiGAZERS hiGAZERS / Tether Tether 	HIGAZERS/USDT
# 0.2% 	$9,781 	$10,305 	6 	Ethernity Chain Etherni... / Tether Tether 	ERN/USDT
# 0.21% 	$10,857 	$17,774 	559 	Perpetual Protocol Perpetu... / Tether Tether 	PERP/USDT
# 0.21% 	$11,815 	$5,715 	522 	Energy Web Energy Web / Bitcoin Bitcoin 	EWT/BTC
# 0.21% 	$17,109 	$12,306 	600 	Tether (USDT) Tether 	USDT/GBP
# 0.21% 	$2,434 	$6,099 	381 	HAPI HAPI / Tether Tether 	HAPI/USDT
# 0.21% 	$24,298 	$23,173 	282 	XCAD Network XCAD Ne... / Tether Tether 	XCAD/USDT
# 0.21% 	$4,595 	$25,648 	436 	Persistence Persist... / Tether Tether 	XPRT/USDT
# 0.21% 	$5,941 	$17,029 	120 	Aleph Zero Aleph Zero / Tether Tether 	AZERO/USDT
# 0.21% 	$724 	$3,055 	245 	ARCS ARCS / Tether Tether 	ARX/USDT
# 0.21% 	$8,442 	$17,389 	406 	Bonfida Bonfida / Tether Tether 	FIDA/USDT
# 0.21% 	$9,493 	$10,910 	680 	BNB BNB / KuCoin KuCoin 	BNB/KCS
# 0.22% 	$1,152 	$3,864 	333 	IOI IOI / Tether Tether 	IOI/USDT
# 0.22% 	$13,437 	$11,624 	360 	WAX WAX / Tether Tether 	WAXP/USDT
# 0.22% 	$15,078 	$33,527 	345 	ARPA ARPA / Tether Tether 	ARPA/USDT
# 0.22% 	$3,412 	$15,420 	306 	NEM NEM / Tether Tether 	XEM/USDT
# 0.22% 	$3,949 	$5,809 	595 	Sweatcoin (Sweat Economy) Sweatco... / Tether Tether 	SWEAT/USDT
# 0.22% 	$3,983 	$6,525 	352 	Dfyn Network Dfyn Ne... / Tether Tether 	DFYN/USDT
# 0.22% 	$359 	$1,517 	474 	Konomi Network Konomi ... / Tether Tether 	KONO/USDT
# 0.22% 	$4,071 	$5,873 	573 	Lattice Lattice / Tether Tether 	LTX/USDT
# 0.22% 	$4,873 	$5,988 	452 	Radio Caca Radio Caca / Tether Tether 	RACA/USDT
# 0.22% 	$443 	$2,503 	563 	Swash Swash / Tether Tether 	SWASH/USDT
# 0.22% 	$5,097 	$7,645 	417 	Verasity Verasity / USD Coin USD Coin 	VRA/USDC
# 0.22% 	$5,807 	$16,379 	542 	Zcash Zcash / Bitcoin Bitcoin 	ZEC/BTC
# 0.22% 	$628 	$5,135 	254 	Hacken Hacken / Tether Tether 	HAI/USDT
# 0.22% 	$839 	$4,750 	101 	FALCONS FALCONS / Tether Tether 	FALCONS/USDT
# 0.22% 	$938 	$5,093 	209 	hiFIDENZA hiFIDENZA / Tether Tether 	HIFIDENZA/...
# 0.23% 	$1,349 	$693 	695 	Travala.com Travala... / Ethereum Ethereum 	AVA/ETH
# 0.23% 	$1,822 	$15,205 	273 	Streamr Streamr / Tether Tether 	DATA/USDT
# 0.23% 	$10,790 	$17,590 	724 	VeChain VeChain / Bitcoin Bitcoin 	VET/BTC
# 0.23% 	$11,960 	$5,578 	473 	Tezos Tezos / Bitcoin Bitcoin 	XTZ/BTC
# 0.23% 	$2,994 	$1,028 	696 	Pirate Chain Pirate ... / Tether Tether 	ARRR/USDT
# 0.23% 	$3,462 	$743 	693 	Bolt Bolt / Tether Tether 	BOLT/USDT
# 0.23% 	$4,017 	$5,287 	717 	Gifto Gifto / Tether Tether 	GFT/USDT
# 0.23% 	$43,808 	$88,851 	111 	Flare Flare / Tether Tether 	FLR/USDT
# 0.23% 	$5,972 	$36,076 	481 	Verasity Verasity / Bitcoin Bitcoin 	VRA/BTC
# 0.23% 	$6,344 	$11,115 	568 	SingularityDAO Singula... / Ethereum Ethereum 	SDAO/ETH
# 0.23% 	$632 	$805 	632 	xHashtag xHashtag / Tether Tether 	XTAG/USDT
# 0.23% 	$8,049 	$22,215 	274 	Illuvium Illuvium / Tether Tether 	ILV/USDT
# 0.23% 	$9,467 	$5,778 	63 	Dego Finance Dego Fi... / Tether Tether 	DEGO/USDT
# 0.23% 	$9,595 	$22,958 	431 	Ontology Ontology / Tether Tether 	ONT/USDT
# 0.23% 	$9,664 	$14,585 	637 	Vulcan Forged Vulcan ... / Bitcoin Bitcoin 	PYR/BTC
# 0.24% 	$11,087 	$9,082 	337 	FTX FTX / Tether Tether 	FTT/USDT
# 0.24% 	$11,243 	$25,740 	515 	iExec RLC iExec RLC / Tether Tether 	RLC/USDT
# 0.24% 	$12,174 	$29,195 	68 	Onyxcoin Onyxcoin / Tether Tether 	XCN/USDT
# 0.24% 	$14,195 	$22,308 	483 	Celer Network Celer N... / Tether Tether 	CELR/USDT
# 0.24% 	$269 	$1,508 	170 	hiCOOLCATS hiCOOLCATS / Tether Tether 	HICOOLCATS...
# 0.24% 	$3,347 	$6,252 	457 	ClinTex CTi ClinTex... / Tether Tether 	CTI/USDT
# 0.24% 	$3,699 	$2,644 	435 	Forj Forj / Tether Tether 	BONDLY/USDT
# 0.24% 	$381 	$4,779 	324 	Pastel Pastel / Tether Tether 	PSL/USDT
# 0.24% 	$492 	$2,475 	504 	Cryptoindex.com 100 Cryptoi... / Tether Tether 	CIX100/USDT
# 0.24% 	$498 	$6,082 	184 	hiMFERS hiMFERS / Tether Tether 	HIMFERS/USDT
# 0.24% 	$5,739 	$7,875 	312 	Kava Lend Kava Lend / Tether Tether 	HARD/USDT
# 0.24% 	$537 	$3,088 	374 	SOLVE SOLVE / Tether Tether 	SOLVE/USDT
# 0.24% 	$6,174 	$13,026 	737 	SafePal SafePal / Tether Tether 	SFP/USDT
# 0.24% 	$825 	$5,291 	443 	CVI CVI / Bitcoin Bitcoin 	GOVI/BTC
# 0.25% 	$1,127 	$2,559 	413 	GamerCoin GamerCoin / Tether Tether 	GHX/USDT
# 0.25% 	$10,065 	$10,792 	53 	TriasLab TriasLab / Tether Tether 	TRIAS/USDT
# 0.25% 	$12,449 	$2,613 	339 	Cere Network Cere Ne... / Tether Tether 	CERE/USDT
# 0.25% 	$18,153 	$7,143 	390 	Ethereum Ethereum / Dai Dai 	ETH/DAI
# 0.25% 	$18,249 	$28,386 	188 	SingularityDAO Singula... / Tether Tether 	SDAO/USDT
# 0.25% 	$3,877 	$25,382 	88 	AllianceBlock Nexera Allianc... / Tether Tether 	NXRA/USDT
# 0.25% 	$4,583 	$18,502 	508 	Meter Governance Meter G... / Tether Tether 	MTRG/USDT
# 0.25% 	$496 	$9,751 	666 	Cudos Cudos / Tether Tether 	CUDOS/USDT
# 0.25% 	$7,916 	$2,458 	346 	Hot Cross Hot Cross / Tether Tether 	HOTCROSS/USDT
# 0.25% 	$966 	$2,096 	496 	Ferrum Network Ferrum ... / Tether Tether 	FRM/USDT
# 0.26% 	$1,821 	$782 	450 	Sinverse Sinverse / Tether Tether 	SIN/USDT
# 0.26% 	$16,470 	$17,302 	527 	Cartesi Cartesi / Tether Tether 	CTSI/USDT
# 0.26% 	$5,151 	$12,162 	314 	Galxe Galxe / Tether Tether 	GAL/USDT
# 0.26% 	$549 	$4,821 	326 	Unicly Unicly / Tether Tether 	UNIC/USDT
# 0.26% 	$7,022 	$948 	627 	XRP XRP / TrueUSD TrueUSD 	XRP/TUSD
# 0.26% 	$7,786 	$20,603 	58 	Seedify.fund Seedify... / Tether Tether 	SFUND/USDT
# 0.27% 	$12,176 	$14,037 	261 	WINkLink WINkLink / Tether Tether 	WIN/USDT
# 0.27% 	$4,567 	$6,942 	199 	Safe Haven Safe Haven / Tether Tether 	SHA/USDT
# 0.27% 	$487 	$5,472 	294 	DOSE DOSE / USD Coin USD Coin 	DOSE/USDC
# 0.27% 	$6,311 	$15,529 	456 	Polkastarter Polkast... / Tether Tether 	POLS/USDT
# 0.27% 	$7,762 	$24,433 	407 	UBIX Network UBIX Ne... / Ethereum Ethereum 	UBX/ETH
# 0.27% 	$9,626 	$14,689 	232 	DODO DODO / Tether Tether 	DODO/USDT
# 0.28% 	$1,245 	$1,701 	645 	UFO Gaming UFO Gaming / Tether Tether 	UFO/USDT
# 0.28% 	$1,572 	$999 	202 	Credefi Credefi / Tether Tether 	CREDI/USDT
# 0.28% 	$13,111 	$11,262 	422 	LooksRare LooksRare / Tether Tether 	LOOKS/USDT
# 0.28% 	$14,825 	$8,459 	80 	Ultra Ultra / Tether Tether 	UOS/USDT
# 0.28% 	$2,598 	$19,617 	394 	Morpheus Network Morpheu... / Tether Tether 	MNW/USDT
# 0.28% 	$2,637 	$7,497 	221 	Scallop Scallop / Tether Tether 	SCLP/USDT
# 0.28% 	$23,290 	$4,875 	482 	RFOX RFOX / Tether Tether 	RFOX/USDT
# 0.28% 	$3,169 	$7,584 	253 	Arenum Arenum / Tether Tether 	ARNM/USDT
# 0.28% 	$3,428 	$18,518 	123 	Frontier Frontier / Tether Tether 	FRONT/USDT
# 0.28% 	$32,003 	$19,264 	349 	DeFiChain DeFiChain / Tether Tether 	DFI/USDT
# 0.28% 	$335 	$772 	440 	AFKDAO AFKDAO / Tether Tether 	AFK/USDT
# 0.28% 	$4,227 	$6,661 	145 	ABBC ABBC / Tether Tether 	ABBC/USDT
# 0.28% 	$6,745 	$4,076 	687 	Marlin Marlin / Tether Tether 	POND/USDT
# 0.28% 	$7,147 	$22,864 	291 	SSV Network SSV Net... / Tether Tether 	SSV/USDT
# 0.28% 	$8,385 	$5,823 	222 	Oraichain Oraichain / Tether Tether 	ORAI/USDT
# 0.29% 	$1,146 	$1,403 	218 	TXA TXA / Tether Tether 	TXA/USDT
# 0.29% 	$1,219 	$22,856 	391 	DeFiChain DeFiChain / Bitcoin Bitcoin 	DFI/BTC
# 0.29% 	$2,156 	$2,310 	472 	Aurora Aurora / Tether Tether 	AURORA/USDT
# 0.29% 	$3,717 	$14,136 	94 	Dogechain Dogechain / Tether Tether 	DC/USDT
# 0.29% 	$920 	$1,176 	602 	Moonwell Moonwell / Tether Tether 	WELL/USDT
# 0.3% 	$1,427 	$2,132 	323 	Chumbi Valley Chumbi ... / Tether Tether 	CHMB/USDT
# 0.3% 	$2,101 	$992 	514 	AptosLaunch Token AptosLa... / Tether Tether 	ALT/USDT
# 0.3% 	$3,555 	$5,244 	555 	Metahero Metahero / Tether Tether 	HERO/USDT
# 0.3% 	$3,825 	$13,527 	308 	BarnBridge BarnBridge / Tether Tether 	BOND/USDT
# 0.3% 	$591 	$1,863 	626 	CVI CVI / Tether Tether 	GOVI/USDT
# 0.31% 	$1,543 	$953 	586 	Vivid Labs Vivid Labs / Tether Tether 	VID/USDT
# 0.31% 	$2,171 	$4,120 	343 	Phantasma Phantasma / Tether Tether 	SOUL/USDT
# 0.31% 	$3,947 	$11,629 	275 	DAO Maker DAO Maker / Tether Tether 	DAO/USDT
# 0.31% 	$312 	$667 	441 	00 Token 00 Token / Tether Tether 	00/USDT
# 0.31% 	$9,366 	$13,174 	607 	PAX Gold PAX Gold / Bitcoin Bitcoin 	PAXG/BTC
# 0.31% 	$9,838 	$4,505 	710 	Constellation Constel... / Bitcoin Bitcoin 	DAG/BTC
# 0.32% 	$15,957 	$30,458 	54 	Sun Token Sun Token / Tether Tether 	SUN/USDT
# 0.32% 	$15,995 	$15,022 	347 	Biconomy Biconomy / Tether Tether 	BICO/USDT
# 0.32% 	$2,245 	$4,829 	340 	Aurory Aurory / Tether Tether 	AURY/USDT
# 0.32% 	$2,398 	$1,593 	141 	Constellation Constel... / Tether Tether 	DAG/USDT
# 0.32% 	$287 	$6,712 	516 	Polkacity Polkacity / Tether Tether 	POLC/USDT
# 0.32% 	$326 	$3,069 	293 	VEED VEED / Tether Tether 	VEED/USDT
# 0.32% 	$6,273 	$8,022 	288 	UBIX Network UBIX Ne... / Tether Tether 	UBX/USDT
# 0.33% 	$1,441 	$3,383 	114 	Dimitra Dimitra / Tether Tether 	DMTR/USDT
# 0.33% 	$1,909 	$8,379 	740 	Hydra Hydra / Tether Tether 	HYDRA/USDT
# 0.33% 	$2,993 	$2,884 	399 	Paribus Paribus / Tether Tether 	PBX/USDT
# 0.33% 	$287 	$223 	605 	Sakura Sakura / Tether Tether 	SKU/USDT
# 0.33% 	$3,092 	$10,653 	414 	Anchor Protocol Anchor ... / Tether Tether 	ANC/USDT
# 0.33% 	$3,269 	$21,945 	554 	? 	AVAX3L/USDT
# 0.33% 	$5,133 	$13,641 	664 	Rocket Pool Rocket ... / Tether Tether 	RPL/USDT
# 0.33% 	$626 	$720 	246 	Melos Studio Melos S... / Tether Tether 	MELOS/USDT
# 0.33% 	$993 	$1,977 	486 	LavaX Labs LavaX Labs / Tether Tether 	LAVAX/USDT
# 0.34% 	$144 	$408 	735 	FEAR FEAR / Tether Tether 	FEAR/USDT
# 0.34% 	$2,069 	$3,356 	423 	MahaDAO MahaDAO / Tether Tether 	MAHA/USDT
# 0.34% 	$564 	$33,918 	543 	Efinity Efinity / Tether Tether 	EFI/USDT
# 0.34% 	$6,567 	$5,571 	84 	DigitalBits Digital... / Tether Tether 	XDB/USDT
# 0.34% 	$6,605 	$287 	451 	H2O Dao H2O Dao / Tether Tether 	H2O/USDT
# 0.34% 	$654 	$1,530 	575 	GEEQ GEEQ / Tether Tether 	GEEQ/USDT
# 0.35% 	$367 	$3,232 	269 	MoneySwap MoneySwap / Tether Tether 	MSWAP/USDT
# 0.35% 	$5,844 	$10,044 	139 	BENQI BENQI / Tether Tether 	QI/USDT
# 0.36% 	$15,776 	$12,117 	220 	Opulous Opulous / Tether Tether 	OPUL/USDT
# 0.36% 	$2,213 	$1,713 	500 	Velas Velas / Tether Tether 	VLX/USDT
# 0.36% 	$3,866 	$11,411 	718 	DIA DIA / Tether Tether 	DIA/USDT
# 0.36% 	$6,001 	$32,294 	140 	LUKSO LUKSO / Tether Tether 	LYXE/USDT
# 0.36% 	$6,420 	$5,097 	720 	Numeraire Numeraire / Tether Tether 	NMR/USDT
# 0.37% 	$1,343 	$3,182 	427 	BEPRO Network BEPRO N... / Tether Tether 	BEPRO/USDT
# 0.37% 	$2,379 	$2,917 	418 	Covalent Covalent / Tether Tether 	CQT/USDT
# 0.37% 	$2,681 	$3,986 	584 	OriginTrail OriginT... / Tether Tether 	TRAC/USDT
# 0.37% 	$3,604 	$140 	739 	OriginTrail OriginT... / Ethereum Ethereum 	TRAC/ETH
# 0.37% 	$391 	$273 	587 	MiL.k Alliance MiL.k A... / Tether Tether 	MLK/USDT
# 0.37% 	$50,122 	$63,669 	178 	Origin Dollar Origin ... / Bitcoin Bitcoin 	OUSD/BTC
# 0.37% 	$602 	$999 	257 	Victoria VR Victori... / Tether Tether 	VR/USDT
# 0.38% 	$1,948 	$1,731 	377 	Burency Burency / Tether Tether 	BUY/USDT
# 0.38% 	$12,976 	$3,885 	128 	Telcoin Telcoin / Tether Tether 	TEL/USDT
# 0.38% 	$158 	$1,223 	567 	Achain Achain / Tether Tether 	ACT/USDT
# 0.38% 	$4,662 	$3,359 	654 	Stepwatch Stepwatch / Tether Tether 	SWP/USDT
# 0.38% 	$6,043 	$5,020 	534 	TRVL TRVL / Tether Tether 	TRVL/USDT
# 0.39% 	$1,255 	$479 	525 	REVV REVV / Tether Tether 	REVV/USDT
# 0.39% 	$1,492 	$5,753 	475 	Every Game Every Game / Tether Tether 	EGAME/USDT
# 0.39% 	$1,584 	$3,210 	297 	Aurox Aurox / Tether Tether 	URUS/USDT
# 0.39% 	$4,106 	$19,517 	193 	Metis Metis / Tether Tether 	METIS/USDT
# 0.39% 	$4,737 	$3,497 	402 	Elastos Elastos / Tether Tether 	ELA/USDT
# 0.39% 	$504 	$6,799 	211 	Ideaology Ideaology / Tether Tether 	IDEA/USDT
# 0.39% 	$518 	$372 	580 	TE-FOOD TE-FOOD / Tether Tether 	TONE/USDT
# 0.39% 	$8,017 	$3,593 	396 	Zebec Protocol Zebec P... / Tether Tether 	ZBC/USDT
# 0.4% 	$1,419 	$6,122 	548 	Good Games Guild Good Ga... / Tether Tether 	GGG/USDT
# 0.4% 	$1,794 	$996 	674 	Travala.com Travala... / Bitcoin Bitcoin 	AVA/BTC
# 0.4% 	$4,777 	$10,099 	329 	Qredo Qredo / Tether Tether 	QRDO/USDT
# 0.4% 	$540 	$1,231 	648 	Only1 Only1 / Tether Tether 	LIKE/USDT
# 0.41% 	$13,188 	$32,142 	663 	Tether (USDT) Tether 	USDT/BRL
# 0.41% 	$2,363 	$6,242 	536 	Sidus Sidus / Tether Tether 	SIDUS/USDT
# 0.41% 	$3,949 	$18,117 	216 	TrueFi TrueFi / Tether Tether 	TRU/USDT
# 0.41% 	$5,677 	$13,398 	487 	SingularityNET Singula... / Bitcoin Bitcoin 	AGIX/BTC
# 0.41% 	$7,947 	$5,247 	148 	Vaiot Vaiot / Tether Tether 	VAI/USDT
# 0.41% 	$94 	$353 	571 	BOSagora BOSagora / Tether Tether 	BOA/USDT
# 0.42% 	$4,199 	$5,064 	276 	Helium Helium / Tether Tether 	HNT/USDT
# 0.42% 	$6,024 	$618 	521 	Stader Stader / Tether Tether 	SD/USDT
# 0.42% 	$777 	$2,085 	723 	Vivid Labs Vivid Labs / Bitcoin Bitcoin 	VID/BTC
# 0.42% 	$797 	$1,545 	615 	Wanchain Wanchain / Ethereum Ethereum 	WAN/ETH
# 0.43% 	$1,061 	$3,189 	263 	EOSForce EOSForce / Tether Tether 	EOSC/USDT
# 0.43% 	$2,833 	$2,952 	259 	EarthFund EarthFund / Tether Tether 	1EARTH/USDT
# 0.43% 	$288 	$1,093 	449 	dAppstore dAppstore / Tether Tether 	DAPPX/USDT
# 0.43% 	$4,211 	$2,354 	37 	LABSV2 LABSV2 / Tether Tether 	LABSV2/USDT
# 0.43% 	$7,394 	$2,429 	412 	WOM Protocol WOM Pro... / Tether Tether 	WOM/USDT
# 0.43% 	$84 	$4,274 	270 	PREMA PREMA / Tether Tether 	PRMX/USDT
# 0.43% 	$867 	$4,136 	650 	BABB BABB / Ethereum Ethereum 	BAX/ETH
# 0.44% 	$1,618 	$2,067 	621 	Mirror Protocol Mirror ... / Tether Tether 	MIR/USDT
# 0.44% 	$10,367 	$7,568 	507 	Gamium Gamium / Tether Tether 	GMM/USDT
# 0.44% 	$270 	$234 	721 	Prom Prom / Bitcoin Bitcoin 	PROM/BTC
# 0.44% 	$344 	$1,618 	302 	Arker Arker / Tether Tether 	ARKER/USDT
# 0.44% 	$8,481 	$16,484 	644 	Bluzelle Bluzelle / Tether Tether 	BLZ/USDT
# 0.45% 	$1,197 	$64 	668 	ReapChain ReapChain / Tether Tether 	REAP/USDT
# 0.45% 	$1,480 	$3,211 	641 	AIOZ Network AIOZ Ne... / Tether Tether 	AIOZ/USDT
# 0.45% 	$125 	$2,285 	447 	Tower Tower / Tether Tether 	TOWER/USDT
# 0.45% 	$2,203 	$11,533 	633 	Boson Protocol Boson P... / Tether Tether 	BOSON/USDT
# 0.45% 	$622 	$1,056 	544 	The Wasted Lands The Was... / Tether Tether 	WAL/USDT
# 0.46% 	$1,030 	$1,744 	137 	BABB BABB / Tether Tether 	BAX/USDT
# 0.46% 	$2,049 	$3,919 	604 	TriasLab TriasLab / Bitcoin Bitcoin 	TRIAS/BTC
# 0.46% 	$2,951 	$12,944 	731 	Clearpool Clearpool / Tether Tether 	CPOOL/USDT
# 0.46% 	$780 	$4,290 	177 	hiPunks hiPunks / Tether Tether 	HIPUNKS/USDT
# 0.46% 	$809 	$3,541 	386 	Ovr Ovr / Tether Tether 	OVR/USDT
# 0.46% 	$855 	$785 	732 	STEPN Green Satoshi Token on Solana STEPN G... / Tether Tether 	GST-SOL/USDT
# 0.46% 	$997 	$782 	206 	Polytrade Polytrade / Tether Tether 	TRADE/USDT
# 0.47% 	$1,072 	$716 	556 	Wanchain Wanchain / Bitcoin Bitcoin 	WAN/BTC
# 0.47% 	$1,228 	$1,333 	530 	Bullieverse Bulliev... / Tether Tether 	BULL/USDT
# 0.47% 	$1,783 	$476 	387 	Onston Onston / Tether Tether 	ONSTON/USDT
# 0.47% 	$10,094 	$11,173 	382 	Hathor Hathor / Tether Tether 	HTR/USDT
# 0.47% 	$2,444 	$2,069 	579 	Hegic Hegic / Tether Tether 	HEGIC/USDT
# 0.47% 	$625 	$4,102 	594 	FortKnoxster FortKno... / Tether Tether 	FKX/USDT
# 0.48% 	$49,233 	$3,149 	316 	Pluton Pluton / Tether Tether 	PLU/USDT
# 0.48% 	$6,029 	$5,914 	292 	Coinweb Coinweb / Tether Tether 	CWEB/USDT
# 0.48% 	$6,547 	$37,753 	152 	Casper Network Casper ... / Tether Tether 	CSPR/USDT
# 0.49% 	$1,006 	$8,971 	630 	Dero Dero / Tether Tether 	DERO/USDT
# 0.49% 	$1,175 	$6,396 	746 	OriginTrail OriginT... / Bitcoin Bitcoin 	TRAC/BTC
# 0.49% 	$1,268 	$4,100 	448 	Cult DAO Cult DAO / Tether Tether 	CULT/USDT
# 0.49% 	$17,408 	$23,304 	511 	Highstreet Highstreet / Tether Tether 	HIGH/USDT
# 0.49% 	$3,141 	$3,588 	499 	Aurora Chain Aurora ... / Tether Tether 	AOA/USDT
# 0.49% 	$5,458 	$502 	640 	MultiVAC MultiVAC / Tether Tether 	MTV/USDT
# 0.49% 	$5,978 	$2,979 	167 	hiSAND33 hiSAND33 / Tether Tether 	HISAND33/USDT
# 0.49% 	$586 	$3,658 	266 	ABBC ABBC / Bitcoin Bitcoin 	ABBC/BTC
# 0.49% 	$7,540 	$12,855 	736 	Pundi X Pundi X / Tether Tether 	PUNDIX/USDT
# 0.49% 	$870 	$8,252 	258 	Glitch Protocol Glitch ... / Tether Tether 	GLCH/USDT
# 0.5% 	$2,854 	$9,065 	115 	LTO Network LTO Net... / Tether Tether 	LTO/USDT
# 0.5% 	$5,928 	$6,832 	395 	OpenOcean OpenOcean / Tether Tether 	OOE/USDT
# 0.5% 	$821 	$1,054 	364 	XANA XANA / Tether Tether 	XETA/USDT
# 0.51% 	$2,086 	$1,619 	165 	hiBEANZ hiBEANZ / Tether Tether 	HIBEANZ/USDT
# 0.52% 	$1,900 	$4,935 	59 	hiMAYC hiMAYC / Tether Tether 	HIMAYC/USDT
# 0.52% 	$1,939 	$1,745 	154 	hiAZUKI hiAZUKI / Tether Tether 	HIAZUKI/USDT
# 0.52% 	$2,205 	$6,454 	518 	Netvrk Netvrk / Tether Tether 	NTVRK/USDT
# 0.52% 	$2,305 	$10,277 	703 	Rally Rally / Tether Tether 	RLY/USDT
# 0.53% 	$1,050 	$665 	652 	Gold Fever Native Gold Gold Fe... / Tether Tether 	NGL/USDT
# 0.53% 	$1,984 	$13,982 	384 	Sperax Sperax / Tether Tether 	SPA/USDT
# 0.53% 	$2,330 	$3,158 	271 	GraphLinq Protocol GraphLi... / Tether Tether 	GLQ/USDT
# 0.53% 	$720 	$975 	590 	Equalizer Equalizer / Tether Tether 	EQZ/USDT
# 0.53% 	$736 	$13,127 	392 	Step App Step App / Tether Tether 	FITFI/USDT
# 0.54% 	$495 	$2,009 	509 	2crazyNFT 2crazyNFT / Tether Tether 	2CRZ/USDT
# 0.54% 	$658 	$3,102 	272 	Oxen Oxen / Tether Tether 	OXEN/USDT
# 0.55% 	$451 	$1,232 	619 	Ertha Ertha / Tether Tether 	ERTHA/USDT
# 0.55% 	$7,473 	$10,832 	150 	Nakamoto Games Nakamot... / Tether Tether 	NAKA/USDT
# 0.56% 	$1,633 	$666 	181 	hiPENGUINS hiPENGUINS / Tether Tether 	HIPENGUINS...
# 0.56% 	$1,982 	$5,345 	389 	Ethernity Chain Etherni... / Bitcoin Bitcoin 	ERN/BTC
# 0.56% 	$300 	$5,525 	240 	FUSION FUSION / Tether Tether 	FSN/USDT
# 0.56% 	$659 	$1,278 	197 	Beldex Beldex / Bitcoin Bitcoin 	BDX/BTC
# 0.56% 	$998 	$3,153 	432 	CoolMining CoolMining / Tether Tether 	COOHA/USDT
# 0.57% 	$2,949 	$1,287 	608 	XDEFI XDEFI / Tether Tether 	XDEFI/USDT
# 0.57% 	$745 	$2,535 	309 	ZeroSwap ZeroSwap / Tether Tether 	ZEE/USDT
# 0.57% 	$948 	$1,109 	635 	LUKSO LUKSO / Ethereum Ethereum 	LYXE/ETH
# 0.58% 	$1,034 	$3,957 	335 	Decentral Games Decentr... / Tether Tether 	DG/USDT
# 0.58% 	$1,554 	$2,669 	113 	Pixie Pixie / Tether Tether 	PIX/USDT
# 0.58% 	$1,660 	$796 	528 	Deeper Network Deeper ... / Tether Tether 	DPR/USDT
# 0.58% 	$179 	$1,896 	659 	Lithium Finance Lithium... / Tether Tether 	LITH/USDT
# 0.59% 	$1,560 	$1,663 	466 	Monsta Infinite Monsta ... / Tether Tether 	MONI/USDT
# 0.59% 	$124 	$259 	741 	MakiSwap MakiSwap / Tether Tether 	MAKI/USDT
# 0.59% 	$294 	$219 	235 	Rare Ball Potion Rare Ba... / Tether Tether 	RBP/USDT
# 0.59% 	$455 	$263 	430 	Bit Store Bit Store / Tether Tether 	STORE/USDT
# 0.6% 	$1,158 	$3,733 	401 	SUKU SUKU / Tether Tether 	SUKU/USDT
# 0.6% 	$2,720 	$136 	706 	Utrust Utrust / Bitcoin Bitcoin 	UTK/BTC
# 0.6% 	$2,941 	$8,029 	212 	DeXe DeXe / Tether Tether 	DEXE/USDT
# 0.6% 	$360 	$1,414 	510 	VEMP VEMP / USD Coin USD Coin 	VEMP/USDC
# 0.61% 	$1,157 	$732 	376 	Lympo Lympo / Tether Tether 	LYM/USDT
# 0.61% 	$502 	$22,420 	676 	Chiliz Chiliz / Bitcoin Bitcoin 	CHZ/BTC
# 0.61% 	$949 	$135 	358 	OnGo OnGo / Tether Tether 	FTG/USDT
# 0.62% 	$2,078 	$1,144 	726 	Euler Euler / Tether Tether 	EUL/USDT
# 0.62% 	$2,342 	$9,044 	372 	NUM Token NUM Token / Tether Tether 	NUM/USDT
# 0.62% 	$678 	$1,292 	681 	Karura Karura / Tether Tether 	KAR/USDT
# 0.63% 	$1,993 	$742 	749 	Cryowar Cryowar / Tether Tether 	CWAR/USDT
# 0.63% 	$4,075 	$9,460 	671 	Lossless Lossless / Tether Tether 	LSS/USDT
# 0.64% 	$1,056 	$2,911 	348 	Sylo Sylo / Tether Tether 	SYLO/USDT
# 0.64% 	$1,610 	$701 	362 	REV3AL REV3AL / Tether Tether 	REV3L/USDT
# 0.64% 	$2,554 	$442 	105 	SO-COL SO-COL / Tether Tether 	SIMP/USDT
# 0.64% 	$2,925 	$3,544 	380 	SENSO SENSO / Tether Tether 	SENSO/USDT
# 0.64% 	$2,929 	$29,329 	198 	YfDAI.finance YfDAI.f... / Tether Tether 	YF-DAI/USDT
# 0.64% 	$31 	$3,454 	660 	The Forbidden Forest The For... / Tether Tether 	FORESTPLUS...
# 0.65% 	$3,357 	$1,266 	130 	Humans.ai Humans.ai / Tether Tether 	HEART/USDT
# 0.66% 	$11,244 	$8,853 	385 	Syscoin Syscoin / Tether Tether 	SYS/USDT
# 0.66% 	$2,925 	$1,210 	214 	Multiverse Multiverse / Tether Tether 	AI/USDT
# 0.66% 	$9,123 	$11,158 	524 	? 	MANA3L/USDT
# 0.67% 	$1,868 	$11,047 	588 	Centrifuge Centrifuge / Tether Tether 	CFG/USDT
# 0.67% 	$7,102 	$7,896 	428 	Frontier Frontier / Bitcoin Bitcoin 	FRONT/BTC
# 0.68% 	$4,405 	$7,878 	498 	Vectorspace AI Vectors... / Tether Tether 	VXV/USDT
# 0.68% 	$487 	$381 	112 	Super Rare Ball Potion Super R... / Tether Tether 	SRBP/USDT
# 0.68% 	$874 	$1,942 	712 	Franklin Franklin / Tether Tether 	FLY/USDT
# 0.69% 	$322 	$2,393 	243 	Serum Serum / Tether Tether 	SRM/USDT
# 0.69% 	$482 	$2,802 	255 	Tidal Finance Tidal F... / Tether Tether 	TIDAL/USDT
# 0.7% 	$3,996 	$1,492 	342 	JUST Stablecoin JUST St... / Tether Tether 	USDJ/USDT
# 0.7% 	$551 	$3,154 	397 	Sentinel Sentinel / Tether Tether 	DVPN/USDT
# 0.7% 	$555 	$3,100 	186 	hiSEALS hiSEALS / Tether Tether 	HISEALS/USDT
# 0.7% 	$782 	$2,952 	638 	SpaceFalcon SpaceFa... / Tether Tether 	FCON/USDT
# 0.7% 	$782 	$5,937 	51 	Kollect Kollect / Tether Tether 	KOL/USDT
# 0.7% 	$917 	$931 	729 	Syntropy Syntropy / Tether Tether 	NOIA/USDT
# 0.7% 	$986 	$799 	734 	Inflation Hedging Coin Inflati... / Tether Tether 	IHC/USDT
# 0.71% 	$1,730 	$342 	642 	VisionGame VisionGame / Tether Tether 	VISION/USDT
# 0.71% 	$1,742 	$3,309 	636 	Share Share / Tether Tether 	SHR/USDT
# 0.71% 	$1,964 	$195 	715 	WHALE WHALE / Tether Tether 	WHALE/USDT
# 0.71% 	$137 	$215 	330 	Strike Strike / Bitcoin Bitcoin 	STRK/BTC
# 0.71% 	$3,986 	$4,866 	711 	BEPRO Network BEPRO N... / Bitcoin Bitcoin 	BEPRO/BTC
# 0.72% 	$11,554 	$917 	649 	Caduceus Caduceus / Tether Tether 	CMP/USDT
# 0.73% 	$1,904 	$7,526 	334 	Carbon Browser Carbon ... / Tether Tether 	CSIX/USDT
# 0.74% 	$2,940 	$5,310 	244 	Dypius Dypius / Tether Tether 	DYP/USDT
# 0.74% 	$523 	$3,820 	485 	Seascape Crowns Seascap... / Tether Tether 	CWS/USDT
# 0.75% 	$1,048 	$11,445 	191 	Unbound Finance Unbound... / Tether Tether 	UNB/USDT
# 0.75% 	$169 	$1,144 	643 	Revain Revain / Tether Tether 	REV/USDT
# 0.76% 	$3,401 	$5,714 	709 	DigitalBits Digital... / Bitcoin Bitcoin 	XDB/BTC
# 0.76% 	$378 	$258 	501 	Propel Propel / Tether Tether 	PEL/USDT
# 0.76% 	$511 	$2,386 	404 	Sienna [ERC-20] Sienna ... / Tether Tether 	WSIENNA/USDT
# 0.76% 	$540 	$1,224 	686 	NuriFootBall NuriFoo... / Tether Tether 	NRFB/USDT
# 0.77% 	$2,573 	$2,580 	628 	Humanode Humanode / Tether Tether 	HMND/USDT
# 0.77% 	$6,929 	$1,650 	400 	AIPad AIPad / Tether Tether 	AIPAD/USDT
# 0.77% 	$802 	$747 	359 	GensoKishi Metaverse GensoKi... / Tether Tether 	MV/USDT
# 0.78% 	$176 	$108 	646 	Dego Finance Dego Fi... / Ethereum Ethereum 	DEGO/ETH
# 0.78% 	$396 	$1,904 	175 	hiFLUF hiFLUF / Tether Tether 	HIFLUF/USDT
# 0.78% 	$569 	$450 	488 	PhoenixDAO PhoenixDAO / Tether Tether 	PHNX/USDT
# 0.79% 	$1,325 	$1,516 	416 	Curate Curate / Tether Tether 	XCUR/USDT
# 0.79% 	$250 	$500 	557 	Proof Of Liquidity Proof O... / Tether Tether 	POL/USDT
# 0.79% 	$7,299 	$18,275 	728 	Safe Haven Safe Haven / Bitcoin Bitcoin 	SHA/BTC
# 0.79% 	$836 	$4,763 	476 	Voxies Voxies / Tether Tether 	VOXEL/USDT
# 0.8% 	$456 	$2,577 	684 	UniLayer UniLayer / Tether Tether 	LAYER/USDT
# 0.8% 	$497 	$1,206 	317 	XCarnival XCarnival / Tether Tether 	XCV/USDT
# 0.8% 	$897 	$557 	593 	BiFi BiFi / Tether Tether 	BIFI/USDT
# 0.81% 	$1,661 	$7,948 	173 	LockTrip LockTrip / Tether Tether 	LOC/USDT
# 0.81% 	$2,902 	$1,102 	444 	Formation FI Formati... / Tether Tether 	FORM/USDT
# 0.82% 	$171 	$1,673 	434 	Chronicle Chronicle / Tether Tether 	XNL/USDT
# 0.82% 	$237 	$1,579 	738 	Onomy Protocol Onomy P... / Tether Tether 	NOM/USDT
# 0.82% 	$423 	$3,750 	227 	Mechaverse Mechaverse / Tether Tether 	MC/USDT
# 0.82% 	$569 	$2,397 	480 	Student Coin Student... / Tether Tether 	STC/USDT
# 0.82% 	$869 	$4,913 	195 	hiRENGA hiRENGA / Tether Tether 	HIRENGA/USDT
# 0.83% 	$18 	$2,090 	454 	Energi Energi / Bitcoin Bitcoin 	NRG/BTC
# 0.83% 	$282 	$1,298 	705 	Stronghold Stronghold / Tether Tether 	SHX/USDT
# 0.83% 	$954 	$117 	714 	Waves Enterprise Waves E... / Tether Tether 	WEST/USDT
# 0.84% 	$127 	$270 	405 	DeFine DeFine / Tether Tether 	DFA/USDT
# 0.84% 	$153 	$1,047 	470 	Hurricane NFT Hurrica... / Tether Tether 	NHCT/USDT
# 0.85% 	$0 	$1 	549 	Uquid Coin Uquid Coin / Bitcoin Bitcoin 	UQC/BTC
# 0.85% 	$1,844 	$2,749 	438 	Frontrow Frontrow / Tether Tether 	FRR/USDT
# 0.85% 	$2,357 	$501 	484 	Hyve Hyve / Tether Tether 	HYVE/USDT
# 0.85% 	$514 	$3,042 	539 	PUMLx PUMLx / Tether Tether 	PUMLX/USDT
# 0.86% 	$1,485 	$1,213 	672 	PARSIQ PARSIQ / Tether Tether 	PRQ/USDT
# 0.86% 	$2,989 	$1,981 	344 	Taraxa Taraxa / Tether Tether 	TARA/USDT
# 0.86% 	$796 	$5,938 	722 	? 	ARB3S/USDT
# 0.88% 	$290 	$1,249 	704 	pNetwork pNetwork / Tether Tether 	PNT/USDT
# 0.88% 	$3,626 	$139 	523 	Pledge Pledge / Tether Tether 	PLGR/USDT
# 0.88% 	$303 	$2,581 	127 	Forj Forj / Ethereum Ethereum 	BONDLY/ETH
# 0.88% 	$834 	$516 	455 	Enecuum Enecuum / Tether Tether 	ENQ/USDT
# 0.89% 	$2,063 	$2,970 	692 	Camelot Token Camelot... / Tether Tether 	GRAIL/USDT
# 0.89% 	$338 	$576 	284 	Cardstack Cardstack / Tether Tether 	CARD/USDT
# 0.9% 	$212 	$125 	533 	RaceFi RaceFi / Tether Tether 	RACEFI/USDT
# 0.92% 	$359 	$1,973 	403 	AntiMatter AntiMatter / Tether Tether 	MATTER/USDT
# 0.92% 	$435 	$1,256 	315 	Skey Network Skey Ne... / Tether Tether 	SKEY/USDT
# 0.94% 	$29,797 	$32,841 	675 	BABB BABB / Bitcoin Bitcoin 	BAX/BTC
# 0.94% 	$410 	$865 	589 	Position Position / Tether Tether 	POSI/USDT
# 0.94% 	$89 	$3,786 	599 	EpiK Protocol EpiK Pr... / Tether Tether 	EPK/USDT
# 0.95% 	$1,762 	$5,395 	612 	Dero Dero / Bitcoin Bitcoin 	DERO/BTC
# 0.95% 	$367 	$6,059 	118 	Prom Prom / Tether Tether 	PROM/USDT
# 0.95% 	$442 	$9,764 	561 	Ultra Ultra / Bitcoin Bitcoin 	UOS/BTC
# 0.96% 	$4,690 	$1,184 	658 	Akash Network Akash N... / Tether Tether 	AKT/USDT
# 0.98% 	$1,021 	$925 	477 	Alpha DEX Alpha DEX / Tether Tether 	ROAR/USDT
# 0.98% 	$1,365 	$506 	535 	Oxen Oxen / Bitcoin Bitcoin 	OXEN/BTC
# 0.99% 	$34 	$68 	545 	LABSV2 LABSV2 / Ethereum Ethereum 	LABSV2/ETH
# 0.99% 	$596 	$961 	629 	Orbit Chain Orbit C... / Tether Tether 	ORC/USDT
# 1.0% 	$150 	$1,345 	618 	Cashaa Cashaa / Tether Tether 	CAS/USDT
# 1.0% 	$337 	$413 	562 	Geojam Geojam / Tether Tether 	JAM/USDT
# 1.01% 	$240 	$215 	491 	Nord Finance Nord Fi... / Tether Tether 	NORD/USDT
# 1.02% 	$267 	$161 	286 	RED TOKEN RED TOKEN / Tether Tether 	RED/USDT
# 1.02% 	$563 	$942 	669 	Hubble Hubble / Tether Tether 	HBB/USDT
# 1.02% 	$657 	$330 	463 	RazrFi RazrFi / Tether Tether 	SOLR/USDT
# 1.04% 	$652 	$1,967 	331 	Apollo Apollo / Tether Tether 	APL/USDT
# 1.04% 	$66 	$156 	546 	Bit Store Bit Store / Ethereum Ethereum 	STORE/ETH
# 1.07% 	$442 	$3,093 	176 	NAGA NAGA / Tether Tether 	NGC/USDT
# 1.09% 	$1,702 	$859 	371 	RankerDao RankerDao / Tether Tether 	RANKER/USDT
# 1.1% 	$144 	$14 	683 	CPChain CPChain / Ethereum Ethereum 	CPC/ETH
# 1.14% 	$899 	$729 	479 	Oxen Oxen / Ethereum Ethereum 	OXEN/ETH
# 1.16% 	$1,393 	$1,509 	727 	VIDT DAO VIDT DAO / Tether Tether 	VIDT/USDT
# 1.16% 	$340 	$314 	565 	BASIC BASIC / Tether Tether 	BASIC/USDT
# 1.17% 	$1,981 	$1,910 	708 	Polytrade Polytrade / Bitcoin Bitcoin 	TRADE/BTC
# 1.19% 	$1,032 	$3,115 	495 	Formation FI Formati... / Ethereum Ethereum 	FORM/ETH
# 1.19% 	$1,126 	$26 	665 	Avalaunch Avalaunch / Tether Tether 	XAVA/USDT
# 1.21% 	$1,419 	$358 	558 	Standard Protocol Standar... / Tether Tether 	STND/USDT
# 1.22% 	$2,322 	$11,200 	279 	Newscrypto Coin Newscry... / Tether Tether 	NWC/USDT
# 1.22% 	$445 	$10,125 	716 	Injective Injective / Bitcoin Bitcoin 	INJ/BTC
# 1.23% 	$105 	$20 	682 	Cashaa Cashaa / Bitcoin Bitcoin 	CAS/BTC
# 1.3% 	$331 	$750 	492 	Covesting Covesting / Tether Tether 	COV/USDT
# 1.31% 	$314 	$125 	217 	GoMoney2 GoMoney2 / Tether Tether 	GOM2/USDT
# 1.38% 	$33 	$768 	494 	Bifrost Bifrost / Tether Tether 	BFC/USDT
# 1.53% 	$580 	$5 	733 	Carbon Browser Carbon ... / Ethereum Ethereum 	CSIX/ETH
# 1.54% 	$131 	$65 	598 	Curate Curate / Bitcoin Bitcoin 	XCUR/BTC
# 1.54% 	$392 	$838 	168 	hiMEEBITS hiMEEBITS / Tether Tether 	HIMEEBITS/...
# 1.61% 	$1,117 	$963 	719 	Standard Protocol Standar... / Ethereum Ethereum 	STND/ETH
# 1.63% 	$15,046 	$10,604 	361 	Roobee Roobee / Bitcoin Bitcoin 	ROOBEE/BTC
# 1.81% 	$103 	$7,847 	506 	Jarvis+ Jarvis+ / Bitcoin Bitcoin 	JAR/BTC
# 2.15% 	$3,452 	$4,490 	256 	Cappasity Cappasity / Ethereum Ethereum 	CAPP/ETH
# 2.15% 	$4,188 	$4,050 	678 	CPChain CPChain / Bitcoin Bitcoin 	CPC/BTC
# 3.0% 	$47 	$1,702 	691 	Nord Finance Nord Fi... / Bitcoin Bitcoin 	NORD/BTC
