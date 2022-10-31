//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "interfaces/IERC20.sol";
import "@uniswapV2/periphery/contracts/interfaces/IUniswapV2Router01.sol";

contract Swap {

    address public owner;
 
    IERC20 public token0;
    IERC20 public token1;

    IUniswapV2Router01 UniswapV2Router01;

    constructor(address _Router) {
        owner = msg.sender;
        UniswapV2Router01 = IUniswapV2Router01(_Router);
    }

    function SendTokenIn(address _tokenIn, uint _amountIn) 
        internal 
        returns (bool) 
    {
        require(IERC20(_tokenIn).balanceOf(msg.sender) >= _amountIn, "Not enough funds to perform this trade");

        //msg.sender should approve "amountIn" tokenIn to contract.this before swap.
        IERC20(_tokenIn).transferFrom(msg.sender, address(this), _amountIn);
        IERC20(_tokenIn).approve(address(UniswapV2Router01), _amountIn);

        return true;
    }

    function PerformTrade(address _tokenIn, address _tokenOut, uint _amountIn) 
        external  
    {
        require(_tokenIn != _tokenOut, "Token addresses must be different from each other");
        token0 = IERC20(_tokenIn);
        token1 = IERC20(_tokenOut);
        require(SendTokenIn(_tokenIn, _amountIn), "Failed to send input tokens");

        address[] memory path = new address[](2);
        path[0] = address(token0);
        path[1] = address(token1);
        uint[] memory amountOut = UniswapV2Router01.getAmountsOut(_amountIn, path);
        UniswapV2Router01.swapExactTokensForTokens(_amountIn, amountOut[amountOut.length - 1], path, msg.sender, block.timestamp + 15 seconds);

    }

}