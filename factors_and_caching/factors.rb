

class MultipleFactorList
  # Relatively straightforward implementation of a class that takes a list of integers
  # and has a couple of methods for returning hashes of its factors and its multiples
  # that also exist in the given listand has a couple of methods for returning hashes of its factors and its multiples
  # that also exist in the given list.
  def initialize(array = [])
    if array.respond_to?(:each)
      if array.is_a? Hash
        @array = []
        array.each do |key, value|
          @array.append(key)
        end
      end
    elsif
      @array = [array]
    end
  end

  def factor_hash
    hash_of_factors = Hash.new
    @array.each do |number|
      hash_of_factors[number] = self.factors_list number
    end

    hash_of_factors
  end

  def factors_list integer
    @array.select { |num| integer % num == 0 && num != integer }
  end

  def multiple_hash
    hash_of_multiples = Hash.new
    @array.each do |number|
      hash_of_multiples[number] = self.multiples_list number
    end

    hash_of_multiples
  end

  def multiples_list integer
    @array.select { |num| num % integer == 0 && num != integer }
  end
end

class MultipleFactorListCached
  # Cached version which won't do the calculation if it's already present in the Hash
  def initialize(array = [])
    if array.respond_to?(:each)
      @array = array
    elsif
      @array = [array]
    end
  end

  def factor_hash
    hash_of_factors = Hash.new
    @array.each do |number|
      if hash_of_factors[number].nil?
        hash_of_factors[number] = self.factors_list number
      end
    end

    hash_of_factors
  end

  def factors_list integer
    @array.select { |num| integer % num == 0 && num != integer }
  end

  def multiple_hash
    hash_of_multiples = Hash.new
    @array.each do |number|
      if hash_of_multiples[number].nil?
        hash_of_multiples[number] = self.multiples_list number
      end
    end

    hash_of_multiples
  end

  def multiples_list integer
    @array.select { |num| num % integer == 0 && num != integer }
  end
end
