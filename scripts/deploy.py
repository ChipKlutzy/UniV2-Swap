from brownie import Swap, accounts, network, interface, Contract

def main():

# Addresses which we will use to make transactions
    MyAcc = accounts[0]
    weth_whale = accounts[-2]
    dai_whale = accounts[-1]

# Essential Addresses 
    weth_addr = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    dai_addr = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    UniV2Router01 = "0xf164fC0Ec4E93095b804a4795bBe1e041497b92a"

# Interfacing Token Contracts 
    WETH = interface.IERC20(weth_addr)
    DAI = interface.IERC20(dai_addr)
    print("__________Created interface for WETH & DAI_____________\n")

# Deploy Swap Contract
    print("Deploying Swap Contract...............\n")
    SwapInstance = Swap.deploy(UniV2Router01, {'from': MyAcc})
    print("__________Swap Contract Deployed Successfully Sweet_____________\n")
    SwapAddr = SwapInstance.address
    print(f"..........Swap.sol is deployed @ {SwapAddr}...........\n")

# Exchanging WETH for DAI 
    print("Exchanging WETH for DAI..............\n")
    AmountInWETH = int(input("Enter the Amount of WETH to sell : ")) * (10 ** WETH.decimals())
    print("\n")
    print("Getting approval from the owner..........\n")
    WETH.approve(SwapAddr, AmountInWETH, {'from': weth_whale})
    print("Trade on progress.....................\n")
    SwapInstance.PerformTrade(weth_addr, dai_addr, AmountInWETH, {'from': weth_whale})
    weth_whale_dai_bal = DAI.balanceOf(weth_whale)
    Price01 = weth_whale_dai_bal / AmountInWETH
    print(f"............Price of ETH in terms of DAI <ETH to DAI>: {Price01} DAI............")
    print("\n")

# Exchanging DAI for WETH
    print("Exchanging DAI for WETH..............\n")
    AmountInDAI =  Price01 * (10 ** DAI.decimals())
    print("Getting approval from the owner..........\n")
    DAI.approve(SwapAddr, AmountInDAI, {'from': dai_whale})
    print("Trade on progress.....................\n")
    SwapInstance.PerformTrade(dai_addr, weth_addr, AmountInDAI, {'from': dai_whale})
    dai_whale_weth_bal = WETH.balanceOf(dai_whale)
    Price02 = dai_whale_weth_bal # / AmountInDAI
    Price02 /= 10 ** 18
    print(f"............Price of ETH in terms of DAI <DAI to ETH>: {Price02} ETH............")
    print("\n")




    


    
