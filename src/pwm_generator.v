module pwm_generator(
	input  wire [11:0] in,
	input  wire sel,
	input  wire wr_en,
	input  wire clk,
	input  wire rst_n,
	output wire pwm_out
);

	reg pwm_out_s;
	reg [11:0] period_reg;
	reg [11:0] duty_reg;

	assign pwm_out = pwm_out_s;

	always@ (posedge clk or negedge rst_n)begin
	if (rst_n == 1'b0) begin
	    period_reg  <= 0;
	    duty_reg    <= 0;
	end else 
	begin
	    if (en == 1'b1) begin
		if (sel == 1'b1) begin
	        	period_reg  	<= in;
		      end  
		else begin
	      		duty_reg    	<= {{5{1'b0}},in[6:0]};
		end
	    end
	end
	end

	wire [12:0] t_on = (period_reg * duty_reg) / 100;
	reg  [11:0] counter;

	always@ (posedge clk or negedge rst_n) begin
	if((rst_n == 1'b0) || (counter == period_reg-1)) begin
		counter <= 0;
	    end
	else begin
	    if((period_reg != 0) && (duty_reg != 0))
		counter <= counter + 1;
	    if(counter < t_on)
		pwm_out_s  <= 1'b1;
	    else 
		pwm_out_s  <= 1'b0;
	    end
	end

endmodule
